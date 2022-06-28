export default function useQueryKeyFactory({ resources }) {
  const keys = {
    all: [resources],
    lists: () => [...keys.all, 'list'],
    list: (params) => [...keys.lists(), { params }],
    details: () => [...keys.all, 'detail'],
    detail: (id) => [...keys.details(), id],
  }

  return keys
}