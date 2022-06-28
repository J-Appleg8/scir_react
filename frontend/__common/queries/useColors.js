import useQueryFactory from "../query_factory/useQueryFactory";

export default (props) => useQueryFactory({ resources: 'colors', ...props })