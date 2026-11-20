import React, { useEffect, useState } from 'react'
import { predictionsAPI, medicinesAPI } from '../services/api'
import { Brain, AlertTriangle, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'

function Predictions() {
  const [predictions, setPredictions] = useState([])
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(true)
  const [newPrediction, setNewPrediction] = useState({ medicine_id: '', demand_quantity: '' })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [predsRes, medsRes] = await Promise.all([
        predictionsAPI.getAll(),
        medicinesAPI.getAll(),
      ])

      setPredictions(predsRes.data)
      setMedicines(medsRes.data)
    } catch (error) {
      toast.error('Failed to load predictions')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePrediction = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const response = await predictionsAPI.create({
        medicine_id: parseInt(newPrediction.medicine_id),
        demand_quantity: parseInt(newPrediction.demand_quantity),
      })

      setPredictions([response.data, ...predictions])
      setNewPrediction({ medicine_id: '', demand_quantity: '' })
      toast.success('Prediction created!')
    } catch (error) {
      toast.error('Failed to create prediction')
      console.error(error)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'shortage':
        return 'bg-red-100 text-red-800'
      case 'low_stock':
        return 'bg-yellow-100 text-yellow-800'
      case 'available':
        return 'bg-green-100 text-green-800'
      case 'overstocked':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
        <Brain className="text-purple-600" />
        AI Shortage Predictions
      </h1>

      {/* Create Prediction Form */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Create New Prediction</h2>
        <form onSubmit={handleCreatePrediction} className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Medicine</label>
            <select
              value={newPrediction.medicine_id}
              onChange={(e) => setNewPrediction({ ...newPrediction, medicine_id: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
              required
            >
              <option value="">Select medicine...</option>
              {medicines.map((m: any) => (
                <option key={m.id} value={m.id}>
                  {m.medicine_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Demand Quantity</label>
            <input
              type="number"
              value={newPrediction.demand_quantity}
              onChange={(e) => setNewPrediction({ ...newPrediction, demand_quantity: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
              placeholder="Enter quantity"
              required
              min="1"
            />
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition"
            >
              Predict
            </button>
          </div>
        </form>
      </div>

      {/* Predictions List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="text-center py-8 text-gray-600">Loading predictions...</div>
        ) : predictions.length > 0 ? (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Medicine</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Demand</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Available Stock</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Prediction</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {predictions.map((pred: any) => (
                <tr key={pred.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{pred.medicine_name}</td>
                  <td className="px-6 py-4 text-gray-600">{pred.demand_quantity} units</td>
                  <td className="px-6 py-4 text-gray-600">{pred.available_stock} units</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(pred.prediction_status)}`}>
                      {pred.prediction_status.replace('_', ' ').toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{pred.confidence.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="text-center py-8 text-gray-600">
            No predictions yet. Create one to get started!
          </div>
        )}
      </div>
    </div>
  )
}

export default Predictions
