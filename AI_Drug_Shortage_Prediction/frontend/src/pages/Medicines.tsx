import React, { useEffect, useState } from 'react'
import { medicinesAPI } from '../services/api'
import { Plus, Search, AlertTriangle } from 'lucide-react'
import toast from 'react-hot-toast'

function Medicines() {
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)

  useEffect(() => {
    fetchMedicines()
  }, [])

  const fetchMedicines = async () => {
    try {
      const response = await medicinesAPI.getAll()
      setMedicines(response.data)
    } catch (error) {
      toast.error('Failed to load medicines')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const filtered = medicines.filter((m: any) =>
    m.medicine_name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Medicines</h1>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition flex items-center gap-2"
        >
          <Plus size={20} />
          Add Medicine
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-3 text-gray-400" size={20} />
        <input
          type="text"
          placeholder="Search medicines..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
        />
      </div>

      {/* Loading State */}
      {loading ? (
        <div className="text-center py-8 text-gray-600">Loading medicines...</div>
      ) : (
        <>
          {/* Medicines Table */}
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Medicine Name</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Category</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Stock</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Price</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {filtered.map((medicine: any) => (
                  <tr key={medicine.id} className="hover:bg-gray-50 transition">
                    <td className="px-6 py-4 font-medium text-gray-900">{medicine.medicine_name}</td>
                    <td className="px-6 py-4 text-gray-600">{medicine.category}</td>
                    <td className="px-6 py-4 text-gray-600">{medicine.current_stock} units</td>
                    <td className="px-6 py-4 text-gray-600">₹{medicine.price.toFixed(2)}</td>
                    <td className="px-6 py-4">
                      {medicine.current_stock === 0 ? (
                        <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-semibold">
                          Out of Stock
                        </span>
                      ) : medicine.current_stock <= medicine.reorder_level ? (
                        <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold flex items-center gap-1 w-fit">
                          <AlertTriangle size={14} />
                          Low Stock
                        </span>
                      ) : (
                        <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                          In Stock
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {filtered.length === 0 && (
              <div className="text-center py-8 text-gray-600">
                No medicines found
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default Medicines
