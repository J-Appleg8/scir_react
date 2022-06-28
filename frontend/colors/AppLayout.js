import React, { createContext, useContext } from 'react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { ReactQueryDevtools } from 'react-query/devtools'
import { Outlet } from 'react-router-dom'

const queryClient = new QueryClient()

const AppContext = createContext()
export const useAppContext = () => useContext(AppContext)

export default function AppLayout() {
  return (
    <QueryClientProvider client={queryClient}>

      <div className="container mt-8">
        <h1>Colors</h1>
        <Outlet />
      </div>

      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
