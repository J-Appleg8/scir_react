import axios from "axios"
import { useInfiniteQuery, useQuery, useQueryClient } from "react-query"
import useQueryKeyFactory from "./useQueryKeyFactory"

export function useList({ resources, params, version = 'v1' }) {
  const keys = useQueryKeyFactory({ resources })

  const query = useInfiniteQuery(
    keys.list(params),
    () => axios.get(`/api/${version}/${resources}/`, { params }).then(({ data }) => data),
    {
      keepPreviousData: true,
    }
  )

  const data = query.data?.pages?.map(({ results }) => results).flat()

  return { query, data }
}

export function useDetail({ resources, params, id, version = 'v1' }) {
  const keys = useQueryKeyFactory({ resources })

  const queryClient = useQueryClient()

  const placeholderData = queryClient.getQueriesData(resources).map(([keys, items]) => items).flat().filter(Boolean).find(({ id: _id }) => _id == id)

  const query = useQuery(
    keys.detail(id),
    () => axios.get(`/api/${version}/${resources}/${id}`, { params }).then(({ data }) => data),
    { placeholderData }
  )

  return { query, data: query.data }
}

export default function useQueryFactory({ resources, params, version = 'v1' }) {
  const list = useList({ resources, params, version })
  const detail = (id) => useDetail({ resources, params, id, version })

  return { list, detail }
}