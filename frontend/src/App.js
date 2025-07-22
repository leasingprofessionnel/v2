import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Components
const Navbar = ({ activeTab, setActiveTab }) => (
  <nav className="bg-white shadow-lg border-b-4 border-blue-600">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between h-16">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-white to-red-600 bg-clip-text text-transparent">
              CRM LLD Auto 🚗
            </h1>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {['dashboard', 'leads', 'calendar'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === tab
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:bg-blue-100 hover:text-blue-600'
                  }`}
                >
                  {tab === 'dashboard' && '📊 Dashboard'}
                  {tab === 'leads' && '👥 Leads'}
                  {tab === 'calendar' && '📅 Calendrier'}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
);

const StatusBadge = ({ status, color }) => (
  <span
    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white"
    style={{ backgroundColor: color }}
  >
    {status.replace('_', ' ').toUpperCase()}
  </span>
);

const Dashboard = ({ stats, statusColors }) => (
  <div className="p-6">
    <div className="mb-8">
      <h2 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h2>
      <p className="text-gray-600">Vue d'ensemble de votre activité LLD</p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 p-6 rounded-lg text-white">
        <h3 className="text-lg font-semibold mb-2">Total Leads</h3>
        <p className="text-3xl font-bold">{stats.total_leads || 0}</p>
      </div>
      <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-lg text-white">
        <h3 className="text-lg font-semibold mb-2">Accords</h3>
        <p className="text-3xl font-bold">{stats.status_stats?.accord || 0}</p>
      </div>
      <div className="bg-gradient-to-r from-red-500 to-red-600 p-6 rounded-lg text-white">
        <h3 className="text-lg font-semibold mb-2">En cours</h3>
        <p className="text-3xl font-bold">{stats.status_stats?.etude_en_cours || 0}</p>
      </div>
      <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-6 rounded-lg text-white">
        <h3 className="text-lg font-semibold mb-2">Offres</h3>
        <p className="text-3xl font-bold">{stats.status_stats?.offre || 0}</p>
      </div>
    </div>

    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-semibold mb-4 text-gray-900">Pipeline des statuts</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {Object.entries(stats.status_stats || {}).map(([status, count]) => (
          <div key={status} className="text-center p-4 rounded-lg bg-gray-50">
            <StatusBadge status={status} color={statusColors[status]} />
            <p className="text-2xl font-bold mt-2">{count}</p>
            <p className="text-sm text-gray-600">{status.replace('_', ' ')}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

const LeadForm = ({ lead, onSave, onCancel, config }) => {
  const [formData, setFormData] = useState({
    company: { name: '', siret: '', address: '', phone: '', email: '' },
    contact: { first_name: '', last_name: '', email: '', phone: '', position: '' },
    vehicle: { brand: '', model: '', carburant: 'diesel', contract_duration: 36, annual_mileage: 15000 },
    assigned_to_prestataire: '',
    assigned_to_commercial: '',
    ...lead
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const selectedBrandModels = config.car_brands[formData.vehicle.brand] || [];

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-8 mx-auto p-8 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
        <h3 className="text-2xl font-bold mb-6 text-gray-900">
          {lead ? 'Modifier le lead' : 'Nouveau lead'}
        </h3>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Company Section */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-blue-900">🏢 Société</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Nom de la société *"
                value={formData.company.name}
                onChange={(e) => setFormData({
                  ...formData,
                  company: { ...formData.company, name: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="text"
                placeholder="SIRET"
                value={formData.company.siret}
                onChange={(e) => setFormData({
                  ...formData,
                  company: { ...formData.company, siret: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="email"
                placeholder="Email société"
                value={formData.company.email}
                onChange={(e) => setFormData({
                  ...formData,
                  company: { ...formData.company, email: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="tel"
                placeholder="Téléphone société"
                value={formData.company.phone}
                onChange={(e) => setFormData({
                  ...formData,
                  company: { ...formData.company, phone: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Contact Section */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-green-900">👤 Contact</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Prénom *"
                value={formData.contact.first_name}
                onChange={(e) => setFormData({
                  ...formData,
                  contact: { ...formData.contact, first_name: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="text"
                placeholder="Nom *"
                value={formData.contact.last_name}
                onChange={(e) => setFormData({
                  ...formData,
                  contact: { ...formData.contact, last_name: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="email"
                placeholder="Email *"
                value={formData.contact.email}
                onChange={(e) => setFormData({
                  ...formData,
                  contact: { ...formData.contact, email: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="tel"
                placeholder="Téléphone"
                value={formData.contact.phone}
                onChange={(e) => setFormData({
                  ...formData,
                  contact: { ...formData.contact, phone: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Vehicle Section */}
          <div className="bg-red-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-red-900">🚗 Véhicule</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <select
                value={formData.vehicle.brand}
                onChange={(e) => setFormData({
                  ...formData,
                  vehicle: { ...formData.vehicle, brand: e.target.value, model: '' }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Sélectionner une marque</option>
                {Object.keys(config.car_brands || {}).map(brand => (
                  <option key={brand} value={brand}>{brand}</option>
                ))}
              </select>
              
              <select
                value={formData.vehicle.model}
                onChange={(e) => setFormData({
                  ...formData,
                  vehicle: { ...formData.vehicle, model: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                required
                disabled={!formData.vehicle.brand}
              >
                <option value="">Sélectionner un modèle</option>
                {selectedBrandModels.map(model => (
                  <option key={model} value={model}>{model}</option>
                ))}
              </select>

              <select
                value={formData.vehicle.carburant}
                onChange={(e) => setFormData({
                  ...formData,
                  vehicle: { ...formData.vehicle, carburant: e.target.value }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="diesel">Diesel</option>
                <option value="essence">Essence</option>
                <option value="hybride">Hybride</option>
                <option value="electrique">Électrique</option>
              </select>

              <select
                value={formData.vehicle.contract_duration}
                onChange={(e) => setFormData({
                  ...formData,
                  vehicle: { ...formData.vehicle, contract_duration: parseInt(e.target.value) }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                {(config.contract_durations || []).map(duration => (
                  <option key={duration} value={duration}>{duration} mois</option>
                ))}
              </select>

              <select
                value={formData.vehicle.annual_mileage}
                onChange={(e) => setFormData({
                  ...formData,
                  vehicle: { ...formData.vehicle, annual_mileage: parseInt(e.target.value) }
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                {(config.annual_mileages || []).map(mileage => (
                  <option key={mileage} value={mileage}>{mileage.toLocaleString()} km/an</option>
                ))}
              </select>
            </div>
          </div>

          {/* Attribution Section */}
          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-purple-900">🎯 Attribution</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <select
                value={formData.assigned_to_prestataire}
                onChange={(e) => setFormData({
                  ...formData,
                  assigned_to_prestataire: e.target.value
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sélectionner un prestataire</option>
                {(config.prestataires || []).map(prestataire => (
                  <option key={prestataire} value={prestataire}>{prestataire}</option>
                ))}
              </select>

              <select
                value={formData.assigned_to_commercial}
                onChange={(e) => setFormData({
                  ...formData,
                  assigned_to_commercial: e.target.value
                })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sélectionner un commercial</option>
                {(config.commerciaux || []).map(commercial => (
                  <option key={commercial} value={commercial}>{commercial}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex justify-end space-x-4 pt-6">
            <button
              type="button"
              onClick={onCancel}
              className="px-6 py-3 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              {lead ? 'Modifier' : 'Créer'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const LeadsTable = ({ leads, onEdit, onDelete, onStatusChange, statusColors, config }) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden">
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Société</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contact</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Véhicule</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Attribution</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {leads.map((lead) => (
            <tr key={lead.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div>
                  <div className="text-sm font-medium text-gray-900">{lead.company.name}</div>
                  <div className="text-sm text-gray-500">{lead.company.siret}</div>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div>
                  <div className="text-sm font-medium text-gray-900">
                    {lead.contact.first_name} {lead.contact.last_name}
                  </div>
                  <div className="text-sm text-gray-500">{lead.contact.email}</div>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {lead.vehicle.brand} {lead.vehicle.model}
                </div>
                <div className="text-sm text-gray-500">
                  {lead.vehicle.carburant} - {lead.vehicle.contract_duration}mois
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={lead.status}
                  onChange={(e) => onStatusChange(lead.id, e.target.value)}
                  className="text-sm border-none bg-transparent focus:ring-2 focus:ring-blue-500 rounded"
                >
                  <option value="premier_contact">Premier contact</option>
                  <option value="relance">Relance</option>
                  <option value="attribue">Attribué</option>
                  <option value="offre">Offre</option>
                  <option value="attente_document">Attente document</option>
                  <option value="etude_en_cours">Étude en cours</option>
                  <option value="accord">Accord</option>
                  <option value="livree">Livrée</option>
                  <option value="perdu">Perdu</option>
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div>{lead.assigned_to_commercial}</div>
                <div className="text-gray-500">{lead.assigned_to_prestataire}</div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  onClick={() => onEdit(lead)}
                  className="text-blue-600 hover:text-blue-900 mr-3"
                >
                  Modifier
                </button>
                <button
                  onClick={() => onDelete(lead.id)}
                  className="text-red-600 hover:text-red-900"
                >
                  Supprimer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

const LeadsView = ({ leads, config, onRefresh }) => {
  const [showForm, setShowForm] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const handleSave = async (leadData) => {
    try {
      if (editingLead) {
        await axios.put(`${API}/leads/${editingLead.id}`, leadData);
      } else {
        await axios.post(`${API}/leads`, leadData);
      }
      setShowForm(false);
      setEditingLead(null);
      onRefresh();
    } catch (error) {
      console.error('Error saving lead:', error);
      alert('Erreur lors de la sauvegarde');
    }
  };

  const handleDelete = async (leadId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce lead ?')) {
      try {
        await axios.delete(`${API}/leads/${leadId}`);
        onRefresh();
      } catch (error) {
        console.error('Error deleting lead:', error);
        alert('Erreur lors de la suppression');
      }
    }
  };

  const handleStatusChange = async (leadId, newStatus) => {
    try {
      await axios.put(`${API}/leads/${leadId}`, { status: newStatus });
      onRefresh();
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Erreur lors de la mise à jour du statut');
    }
  };

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = !searchTerm || 
      lead.company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.contact.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.contact.last_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = !statusFilter || lead.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-900">Gestion des Leads</h2>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors font-medium"
        >
          ➕ Nouveau Lead
        </button>
      </div>

      <div className="flex space-x-4 mb-6">
        <input
          type="text"
          placeholder="Rechercher..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Tous les statuts</option>
          <option value="premier_contact">Premier contact</option>
          <option value="relance">Relance</option>
          <option value="attribue">Attribué</option>
          <option value="offre">Offre</option>
          <option value="attente_document">Attente document</option>
          <option value="etude_en_cours">Étude en cours</option>
          <option value="accord">Accord</option>
          <option value="livree">Livrée</option>
          <option value="perdu">Perdu</option>
        </select>
      </div>

      <LeadsTable 
        leads={filteredLeads}
        onEdit={(lead) => { setEditingLead(lead); setShowForm(true); }}
        onDelete={handleDelete}
        onStatusChange={handleStatusChange}
        statusColors={config.status_colors}
        config={config}
      />

      {showForm && (
        <LeadForm
          lead={editingLead}
          onSave={handleSave}
          onCancel={() => { setShowForm(false); setEditingLead(null); }}
          config={config}
        />
      )}
    </div>
  );
};

const Calendar = ({ leads }) => (
  <div className="p-6">
    <h2 className="text-3xl font-bold text-gray-900 mb-6">Calendrier & Tâches</h2>
    <div className="bg-white rounded-lg shadow-md p-6">
      <p className="text-gray-600 mb-4">Prochaines tâches et rappels :</p>
      <div className="space-y-4">
        {leads.slice(0, 5).map((lead) => (
          <div key={lead.id} className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
            <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
            <div>
              <p className="font-medium">Relancer {lead.contact.first_name} {lead.contact.last_name}</p>
              <p className="text-sm text-gray-600">{lead.company.name} - {lead.vehicle.brand} {lead.vehicle.model}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

// Main App Component
function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [leads, setLeads] = useState([]);
  const [stats, setStats] = useState({});
  const [config, setConfig] = useState({});
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [leadsRes, statsRes, configRes] = await Promise.all([
        axios.get(`${API}/leads`),
        axios.get(`${API}/dashboard/stats`),
        axios.get(`${API}/config`)
      ]);
      
      setLeads(leadsRes.data);
      setStats(statsRes.data);
      setConfig(configRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du CRM...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main>
        {activeTab === 'dashboard' && (
          <Dashboard stats={stats} statusColors={config.status_colors} />
        )}
        {activeTab === 'leads' && (
          <LeadsView leads={leads} config={config} onRefresh={fetchData} />
        )}
        {activeTab === 'calendar' && (
          <Calendar leads={leads} />
        )}
      </main>
    </div>
  );
}

export default App;