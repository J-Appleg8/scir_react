from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.viewsets import ProjectionsAndFilters
from django.db import transaction
from django.shortcuts import HttpResponse
from core.models import AltSub, AltSubUpload, Program
import pandas as pd

User = get_user_model()


class NoFileError(Exception):
    pass


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = AltSubUpload
            fields = [
                "id",
                "data_file",
            ]

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = AltSubUpload
            fields = [
                "id",
                "sector",
                "data_file",
                "created",
                "uploaded_by",
            ]

    class Create(serializers.ModelSerializer):
        uploaded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

        class Meta:
            model = AltSubUpload
            fields = [
                "id",
                "sector",
                "data_file",
                "uploaded_by",
            ]

        def is_valid(self, raise_exception=False):
            return super().is_valid(raise_exception)

        def create(self, validated_data):
            new_alt_sub_upload = super().create(validated_data)

            # Loading file from request method POST
            try:
                df = pd.read_csv(new_alt_sub_upload.data_file, encoding_errors="ignore", dtype=str)
                df.drop(["Date"], axis=1, inplace=True, errors="ignore")
                df["Created"] = pd.to_datetime(df["Created"], format="%m/%d/%Y", errors="coerce").apply(lambda x: x.date())
                df["Created"] = df["Created"].fillna("None")
                df["Next Higher Assembly"] = df["Next Higher Assembly"].fillna("None")
                df["Type Code"] = df["Type Code"].fillna("NA")
                df["WBS Element"] = df["WBS Element"].fillna("None")
                df["RevLev"] = df["RevLev"].fillna("None")
                df["Item Text Line 1"] = df["Item Text Line 1"].fillna("None")
                df["Model"] = df["Model"].fillna("None")
                df["Created by"] = df["Created by"].fillna("None")
                rows = df.to_dict("records")

                # ################################################################################
                # Building set with existing database entries
                with transaction.atomic():
                    altsub_items = AltSub.objects.filter(upload__sector_id=new_alt_sub_upload.sector_id)
                    db = set(
                        (
                            item.plant,
                            item.model,
                            item.type_code,
                            item.primary_material,
                            item.replacement_part,
                            item.next_higher_assembly,
                            item.alternate_or_substitute_code,
                            item.sub_code,
                            item.wbs_element,
                            item.revision_level,
                            item.reason_for_change,
                            item.item_text_line,
                            item.created_by,
                            item.created_date,
                        )
                        for item in altsub_items
                    )

                # ################################################################################
                # Creating set with data from file upload
                file_data_set = set(
                    (
                        row["Plnt"],
                        row["Model"],
                        row["Type Code"],
                        row["Primary Material"],
                        row["Replacement Part"],
                        row["Next Higher Assembly"],
                        row["Alternate or Substitute Code"],
                        row["Sub Code"],
                        row["WBS Element"],
                        row["RevLev"],
                        row["Reason For Change"],
                        row["Item Text Line 1"],
                        row["Created by"],
                        row["Created"] if row["Created"] != "None" else None,
                    )
                    for row in rows
                )

                # ################################################################################
                # Delete items from database
                items_to_delete = db - file_data_set
                print(f"Items to Delete: {len(items_to_delete)}")

                for (plant, model, typecd, prim_mat, rep_part, nha, altsubcd, subcd, wbs, revlev, res_chng, itemtxt, createdby, creatd) in items_to_delete:
                    AltSub.objects.filter(plant=plant).filter(model=model).filter(type_code=typecd).filter(primary_material_id=prim_mat).filter(
                        replacement_part_id=rep_part
                    ).delete()

                # ################################################################################
                # Add items to database - Create list of dictionaries for the new items to add
                items_to_add = file_data_set - db
                print(f"Items to Add: {len(items_to_add)}")
                items_to_add_list_dict = []

                for (plant, model, typecd, prim_mat, rep_part, nha, altsubcd, subcd, wbs, revlev, res_chng, itemtxt, createdby, creatd) in items_to_add:
                    new_dict = {}
                    new_dict["Plnt"] = (plant,)
                    new_dict["Model"] = (model,)
                    new_dict["Type Code"] = (typecd,)
                    new_dict["Primary Material"] = (prim_mat,)
                    new_dict["Replacement Part"] = (rep_part,)
                    new_dict["Next Higher Assembly"] = (nha,)
                    new_dict["Alternate or Substitute Code"] = (altsubcd,)
                    new_dict["Sub Code"] = (subcd,)
                    new_dict["WBS Element"] = (wbs,)
                    new_dict["RevLev"] = (revlev,)
                    new_dict["Reason For Change"] = (res_chng,)
                    new_dict["Item Text Line 1"] = (itemtxt,)
                    new_dict["Created by"] = (createdby,)
                    new_dict["Created"] = creatd
                    items_to_add_list_dict.append(new_dict)

                # ################################################################################
                # Bulk Update items to Database
                with transaction.atomic():
                    distinct_model_for_altsubs = {(row["Model"] if row["Model"] else None) for row in items_to_add_list_dict}

                    for i, model in enumerate(distinct_model_for_altsubs):
                        rows_for_altsubs = list(filter(lambda x: x["Model"] == model, items_to_add_list_dict))
                        new_altsub_items = []

                        for row in rows_for_altsubs:
                            program_model = Program.objects.get(model_code=str(row["Model"]))

                            new_altsub_items.append(
                                AltSub(
                                    plant=row["Plnt"],
                                    model=program_model,
                                    type_code=row["Type Code"],
                                    primary_material_id=row["Primary Material"],
                                    replacement_part_id=row["Replacement Part"],
                                    next_higher_assembly=row["Next Higher Assembly"],
                                    alternate_or_substitute_code=row["Alternate or Substitute Code"],
                                    sub_code=row["Sub Code"],
                                    wbs_element=row["WBS Element"],
                                    revision_level=row["RevLev"],
                                    reason_for_change=row["Reason for Change"],
                                    item_text_line=row["Item Text Line 1"],
                                    created_by=row["Created by"],
                                    created_date=row["Cretaed"],
                                    upload=new_alt_sub_upload,
                                )
                            )

                        AltSub.objects.bulk_create(new_altsub_items)

            except NoFileError as e:
                return HttpResponse(str(e), status=400)

            return new_alt_sub_upload

    for_ = {
        "summary": Summary,
        "detail": Detail,
        "POST": Create,
    }


class ViewSet(ProjectionsAndFilters):
    queryset = AltSubUpload.objects.all()
    serializers = Serializers
    serializer_class = Serializers.Detail

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
