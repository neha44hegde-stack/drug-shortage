import React, { useEffect, useState } from 'react'
import { salesAPI, medicinesAPI } from '../services/api'
import { ShoppingCart, Plus } from 'lucide-react'
import toast from 'react-hot-toast'

function Sales() {
  const [sales, setSales] = useState([])
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({ total_transactions: 0, total_quantity: 0, total_amount: 0 })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [salesRes, statsRes, medsRes] = await Promise.all([
        salesAPI.getAll(0, 50),
        salesAPI.getTodayStats(),
        medicinesAPI.getAll(0, 100),
      ])

      setSales(salesRes.data)
      setStats(statsRes.data)
      setMedicines(medsRes.data)
    } catch (error) {
      toast.error('Failed to load sales data')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Sales</h1>
        <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition flex items-center gap-2">
          <Plus size={20} />
          New Sale
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Transactions Today</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">{stats.total_transactions}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Units Sold</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">{stats.total_quantity}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Amount</p>
          <p className="text-3xl font-bold text-green-600 mt-2">₹{stats.total_amount.toFixed(2)}</p>
        </div>
      </div>

      {/* Sales Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Medicine</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Quantity</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Unit Price</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Total</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {sales.map((sale: any) => (
              <tr key={sale.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 font-medium text-gray-900">{sale.medicine_name}</td>
                <td className="px-6 py-4 text-gray-600">{sale.quantity} units</td>
                <td className="px-6 py-4 text-gray-600">₹{sale.unit_price.toFixed(2)}</td>
                <td className="px-6 py-4 font-semibold text-green-600">₹{sale.total_amount.toFixed(2)}</td>
                <td className="px-6 py-4 text-gray-600">
                  {new Date(sale.sale_date).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {sales.length === 0 && (
          <div className="text-center py-8 text-gray-600">
            No sales recorded yet
          </div>
        )}
      </div>
    </div>
  )
}

export default Sales
