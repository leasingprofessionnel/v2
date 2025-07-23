import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Components
const Navbar = ({ activeTab, setActiveTab }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-600 via-white to-red-600 bg-clip-text text-transparent">
              CRM LEASINPROFESSIONNEL.FR
            </h1>
          </div>
          
          {/* Navigation Desktop */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {['dashboard', 'leads', 'clients', 'calendar', 'backup'].map((tab) => (
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
                  {tab === 'clients' && '🎯 Clients'}
                  {tab === 'calendar' && '📅 Calendrier'}
                  {tab === 'backup' && '💾 Sauvegardes'}
                </button>
              ))}
            </div>
          </div>

          {/* Bouton Menu Mobile */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-blue-600 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <svg className="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Menu Mobile */}
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-gray-50 rounded-lg mt-2">
              {['dashboard', 'leads', 'clients', 'calendar', 'backup'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => {
                    setActiveTab(tab);
                    setMobileMenuOpen(false);
                  }}
                  className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors ${
                    activeTab === tab
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:bg-blue-100 hover:text-blue-600'
                  }`}
                >
                  {tab === 'dashboard' && '📊 Dashboard'}
                  {tab === 'leads' && '👥 Leads'}
                  {tab === 'clients' && '🎯 Clients'}
                  {tab === 'calendar' && '📅 Calendrier'}
                  {tab === 'backup' && '💾 Sauvegardes'}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

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

    {/* Statistics Cards */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
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

    {/* Commission Statistics */}
    {stats.commissions_stats && (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 p-6 rounded-lg text-white">
          <h3 className="text-lg font-semibold mb-2">💰 Commissions Payées {stats.commissions_stats.year}</h3>
          <p className="text-3xl font-bold">{stats.commissions_stats.total_paid}€</p>
          <p className="text-sm opacity-90">Commissions encaissées cette année</p>
        </div>
        <div className="bg-gradient-to-r from-orange-500 to-orange-600 p-6 rounded-lg text-white">
          <h3 className="text-lg font-semibold mb-2">⏳ Commissions En Attente {stats.commissions_stats.year}</h3>
          <p className="text-3xl font-bold">{stats.commissions_stats.total_pending}€</p>
          <p className="text-sm opacity-90">Commissions à recevoir</p>
        </div>
      </div>
    )}

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

const ReminderForm = ({ leadId, onSave, onCancel }) => {
  const [reminderData, setReminderData] = useState({
    title: '',
    description: '',
    reminder_date: new Date().toISOString().slice(0, 16), // Default to now
    priority: 'medium',
    reminder_type: 'general'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      ...reminderData,
      lead_id: leadId,
      reminder_date: new Date(reminderData.reminder_date).toISOString()
    });
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full mx-4">
        <h3 className="text-lg font-bold mb-4">📅 Ajouter un rappel</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Titre du rappel *"
            value={reminderData.title}
            onChange={(e) => setReminderData({ ...reminderData, title: e.target.value })}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            required
          />
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priorité</label>
              <select
                value={reminderData.priority}
                onChange={(e) => setReminderData({ ...reminderData, priority: e.target.value })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="low">📝 Faible</option>
                <option value="medium">📋 Normal</option>
                <option value="high">⚡ Prioritaire</option>
                <option value="urgent">🚨 Urgent</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Type</label>
              <select
                value={reminderData.reminder_type}
                onChange={(e) => setReminderData({ ...reminderData, reminder_type: e.target.value })}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="general">📝 Général</option>
                <option value="call">📞 Appel</option>
                <option value="email">✉️ Email</option>
                <option value="meeting">🤝 Rendez-vous</option>
                <option value="follow_up">📋 Suivi</option>
              </select>
            </div>
          </div>
          
          <textarea
            placeholder="Description (optionnel)"
            value={reminderData.description}
            onChange={(e) => setReminderData({ ...reminderData, description: e.target.value })}
            rows="3"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date et heure du rappel *
            </label>
            <input
              type="datetime-local"
              value={reminderData.reminder_date}
              onChange={(e) => setReminderData({ ...reminderData, reminder_date: e.target.value })}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const LeadForm = ({ lead, onSave, onCancel, config }) => {
  const [formData, setFormData] = useState({
    company: { name: '', siret: '', address: '', phone: '', email: '' },
    contact: { first_name: '', last_name: '', email: '', phone: '', position: '' },
    vehicles: [{ 
      brand: '', model: '', carburant: 'diesel', contract_duration: 36, annual_mileage: 15000,
      tarif_mensuel: '', commission_agence: '', payment_status: 'en_attente'
    }],
    note: '',
    status: 'premier_contact', // Nouveau champ pour modifier le statut
    lead_creation_date: new Date().toISOString().split('T')[0], // Date du jour par défaut
    assigned_to_prestataire: '',
    assigned_to_commercial: '',
    delivery_date: '', // Date de livraison
    contract_end_date: '', // Date de fin de contrat (calculée)
    ...lead
  });

  const [vehicleCount, setVehicleCount] = useState(1);
  const [showReminderForm, setShowReminderForm] = useState(false);

  useEffect(() => {
    if (lead && lead.vehicles) {
      setVehicleCount(lead.vehicles.length);
    }
  }, [lead]);

  // Auto-calculate contract end date when delivery date or contract duration changes
  useEffect(() => {
    if (formData.delivery_date && formData.vehicles.length > 0 && formData.vehicles[0].contract_duration) {
      const deliveryDate = new Date(formData.delivery_date);
      const contractMonths = formData.vehicles[0].contract_duration;
      const endDate = new Date(deliveryDate);
      endDate.setMonth(endDate.getMonth() + contractMonths);
      
      setFormData(prev => ({
        ...prev,
        contract_end_date: endDate.toISOString().split('T')[0]
      }));
    }
  }, [formData.delivery_date, formData.vehicles]);

  // Auto-set delivery date when status changes to "accord"
  useEffect(() => {
    if (formData.status === 'accord' && !formData.delivery_date) {
      const today = new Date().toISOString().split('T')[0];
      setFormData(prev => ({ ...prev, delivery_date: today }));
    }
  }, [formData.status]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleVehicleCountChange = (newCount) => {
    setVehicleCount(newCount);
    const vehicles = [...formData.vehicles];
    
    if (newCount > vehicles.length) {
      // Add new vehicles
      for (let i = vehicles.length; i < newCount; i++) {
        vehicles.push({ 
          brand: '', model: '', carburant: 'diesel', contract_duration: 36, annual_mileage: 15000,
          tarif_mensuel: '', commission_agence: '', payment_status: 'en_attente'
        });
      }
    } else {
      // Remove excess vehicles
      vehicles.splice(newCount);
    }
    
    setFormData({ ...formData, vehicles });
  };

  const updateVehicle = (index, field, value) => {
    const vehicles = [...formData.vehicles];
    vehicles[index] = { ...vehicles[index], [field]: value };
    
    // Reset model when brand changes
    if (field === 'brand') {
      vehicles[index].model = '';
    }
    
    setFormData({ ...formData, vehicles });
  };

  const handleAddReminder = async (reminderData) => {
    try {
      await axios.post(`${API}/reminders`, reminderData);
      setShowReminderForm(false);
      alert('Rappel ajouté avec succès !');
    } catch (error) {
      console.error('Error creating reminder:', error);
      alert('Erreur lors de l\'ajout du rappel');
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await axios.get(`${API}/leads/${lead.id}/pdf`, {
        responseType: 'blob'
      });
      
      // Create blob link to download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from response headers or use default
      const contentDisposition = response.headers['content-disposition'];
      let filename = `Lead_${lead.company.name.replace(/[^a-zA-Z0-9]/g, '_')}_${lead.id.slice(0, 8)}.pdf`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Erreur lors du téléchargement du PDF');
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-8 mx-auto p-8 border w-11/12 max-w-6xl shadow-lg rounded-md bg-white max-h-screen overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-2xl font-bold text-gray-900">
            {lead ? 'Modifier le lead' : 'Nouveau lead'}
          </h3>
          {lead && (
            <div className="flex space-x-3">
              <button
                type="button"
                onClick={() => handleDownloadPDF()}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors flex items-center"
              >
                📄 Télécharger PDF
              </button>
              <button
                type="button"
                onClick={() => setShowReminderForm(true)}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
              >
                📅 Ajouter un rappel
              </button>
            </div>
          )}
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Date de création du lead - En haut */}
          <div className="bg-gray-50 p-4 rounded-lg border-2 border-gray-200">
            <div className="flex items-center space-x-4">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  📅 Date de création du lead
                </label>
                <input
                  type="date"
                  value={formData.lead_creation_date || ''}
                  onChange={(e) => setFormData({ ...formData, lead_creation_date: e.target.value })}
                  className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
                <p className="font-medium text-blue-800 mb-1">💡 Information</p>
                <p>Cette date permet de trier et filtrer vos leads par date de création.</p>
                <p className="text-xs mt-1">Par défaut: date du jour</p>
              </div>
            </div>
          </div>

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

          {/* Status Section - Nouveau */}
          <div className="bg-indigo-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-indigo-900">📊 Statut du Lead</h4>
            <select
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value="a_contacter">🔴 À contacter</option>
              <option value="premier_contact">Premier contact</option>
              <option value="relance">Relance</option>
              <option value="attribue">Attribué</option>
              <option value="offre">Offre</option>
              <option value="attente_document">Attente document</option>
              <option value="etude_en_cours">Étude en cours</option>
              <option value="accord">Accord</option>
              <option value="livree">🟢 Livrée</option>
              <option value="perdu">Perdu</option>
            </select>
          </div>

          {/* Vehicle Count Selection */}
          <div className="bg-yellow-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-yellow-900">🔢 Nombre de véhicules</h4>
            <select
              value={vehicleCount}
              onChange={(e) => handleVehicleCountChange(parseInt(e.target.value))}
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value={0}>0 véhicule (à définir plus tard)</option>
              {Array.from({length: 20}, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num} véhicule{num > 1 ? 's' : ''}</option>
              ))}
            </select>
          </div>

          {/* Vehicles Section - Affichée seulement si vehicleCount > 0 */}
          {vehicleCount > 0 ? (
            <div className="bg-red-50 p-4 rounded-lg">
              <h4 className="text-lg font-semibold mb-3 text-red-900">🚗 Véhicules</h4>
              {formData.vehicles.map((vehicle, index) => {
                const selectedBrandModels = config.car_brands?.[vehicle.brand] || [];
                return (
                  <div key={index} className="border-2 border-red-200 p-4 rounded-lg mb-4 bg-white">
                    <h5 className="font-medium text-red-800 mb-3">Véhicule {index + 1}</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Marque véhicule <span className="text-gray-400">(optionnel)</span>
                      </label>
                      <select
                        value={vehicle.brand}
                        onChange={(e) => updateVehicle(index, 'brand', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">🚗 Pas encore défini</option>
                        {Object.keys(config.car_brands || {}).map(brand => (
                          <option key={brand} value={brand}>{brand}</option>
                        ))}
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Modèle véhicule <span className="text-gray-400">(optionnel)</span>
                      </label>
                      <select
                        value={vehicle.model}
                        onChange={(e) => updateVehicle(index, 'model', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                        disabled={!vehicle.brand}
                      >
                        <option value="">
                          {vehicle.brand ? "Sélectionner un modèle" : "Choisir d'abord une marque"}
                        </option>
                        {selectedBrandModels.map(model => (
                          <option key={model} value={model}>{model}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Carburant <span className="text-gray-400">(optionnel)</span>
                      </label>
                      <select
                        value={vehicle.carburant}
                        onChange={(e) => updateVehicle(index, 'carburant', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">À définir</option>
                        <option value="diesel">Diesel</option>
                        <option value="essence">Essence</option>
                        <option value="hybride">Hybride</option>
                        <option value="electrique">Électrique</option>
                      </select>
                    </div>

                    <select
                      value={vehicle.contract_duration}
                      onChange={(e) => updateVehicle(index, 'contract_duration', parseInt(e.target.value))}
                      className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                    >
                      {(config.contract_durations || []).map(duration => (
                        <option key={duration} value={duration}>{duration} mois</option>
                      ))}
                    </select>

                    <select
                      value={vehicle.annual_mileage}
                      onChange={(e) => updateVehicle(index, 'annual_mileage', parseInt(e.target.value))}
                      className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                    >
                      {(config.annual_mileages || []).map(mileage => (
                        <option key={mileage} value={mileage}>{mileage.toLocaleString()} km/an</option>
                      ))}
                    </select>

                    {/* Nouveaux champs sur la même ligne */}
                    <input
                      type="text"
                      placeholder="Tarif mensuel"
                      value={vehicle.tarif_mensuel || ''}
                      onChange={(e) => updateVehicle(index, 'tarif_mensuel', e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  {/* Champs Commission - Affichés seulement si statut = accord ou livree */}
                  {(formData.status === 'accord' || formData.status === 'livree') && (
                    <div className="mt-3">
                      <div className="bg-amber-50 p-3 rounded-lg border-l-4 border-amber-400 mb-3">
                        <p className="text-sm text-amber-800 font-medium">
                          💰 Section Commission (disponible car statut: {formData.status === 'accord' ? 'Accord' : 'Livrée'})
                        </p>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Commission agence
                          </label>
                          <input
                            type="text"
                            placeholder="ex: 800€"
                            value={vehicle.commission_agence || ''}
                            onChange={(e) => updateVehicle(index, 'commission_agence', e.target.value)}
                            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                        
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Statut paiement commission
                          </label>
                          <select
                            value={vehicle.payment_status || 'en_attente'}
                            onChange={(e) => updateVehicle(index, 'payment_status', e.target.value)}
                            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                          >
                            <option value="en_attente">💰 En attente</option>
                            <option value="paye">✅ Payé</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Message informatif si statut ne permet pas les commissions */}
                  {formData.status !== 'accord' && formData.status !== 'livree' && (
                    <div className="mt-3 bg-blue-50 p-3 rounded-lg border-l-4 border-blue-400">
                      <p className="text-sm text-blue-800">
                        ℹ️ Les champs de commission apparaîtront une fois le statut passé à <strong>"Accord"</strong> ou <strong>"Livrée"</strong>
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          ) : (
            <div className="bg-gray-50 p-4 rounded-lg border-2 border-dashed border-gray-300">
              <div className="text-center py-6">
                <div className="text-4xl text-gray-400 mb-3">🚗</div>
                <h4 className="text-lg font-medium text-gray-600 mb-2">Aucun véhicule spécifié</h4>
                <p className="text-sm text-gray-500">
                  Vous pourrez ajouter les détails du véhicule plus tard en modifiant ce lead
                </p>
              </div>
            </div>
          )}

          {/* Note Section */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold mb-3 text-gray-900">📝 Note</h4>
            <textarea
              placeholder="Commentaires ou informations complémentaires..."
              value={formData.note}
              onChange={(e) => setFormData({ ...formData, note: e.target.value })}
              rows="4"
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 resize-vertical"
            />
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

          {/* Dates importantes Section - Affichée pour accord ou livree */}
          {(formData.status === 'accord' || formData.status === 'livree' || formData.delivery_date || formData.contract_end_date) && (
            <div className="bg-amber-50 p-4 rounded-lg">
              <h4 className="text-lg font-semibold mb-3 text-amber-900">
                📅 Dates importantes
                {formData.status === 'livree' && <span className="ml-2 text-green-700">(Véhicule livré)</span>}
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    📅 Date de livraison {(formData.status === 'accord' || formData.status === 'livree') && '*'}
                  </label>
                  <input
                    type="date"
                    value={formData.delivery_date || ''}
                    onChange={(e) => {
                      const newFormData = { ...formData, delivery_date: e.target.value };
                      
                      // Calcul automatique de la date de fin de contrat
                      if (e.target.value && formData.vehicles.length > 0 && formData.vehicles[0].contract_duration) {
                        const deliveryDate = new Date(e.target.value);
                        const contractDuration = parseInt(formData.vehicles[0].contract_duration);
                        const contractEndDate = new Date(deliveryDate);
                        contractEndDate.setMonth(contractEndDate.getMonth() + contractDuration);
                        newFormData.contract_end_date = contractEndDate.toISOString().split('T')[0];
                      }
                      
                      setFormData(newFormData);
                    }}
                    className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                    disabled={formData.status !== 'accord' && formData.status !== 'livree'}
                    required={formData.status === 'livree'}
                  />
                  {formData.status === 'livree' && !formData.delivery_date && (
                    <p className="text-sm text-red-600 mt-1">Date de livraison requise pour statut "Livré"</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    📅 Date de fin de contrat 
                    {formData.vehicles[0]?.contract_duration && (
                      <span className="text-sm text-gray-500">
                        (+ {formData.vehicles[0].contract_duration} mois)
                      </span>
                    )}
                  </label>
                  <input
                    type="date"
                    value={formData.contract_end_date || ''}
                    className="w-full p-3 border border-gray-300 rounded-md bg-gray-100 text-gray-600"
                    disabled
                    placeholder="Calculé automatiquement"
                  />
                  {formData.contract_end_date && (
                    <p className="text-sm text-green-600 mt-1">
                      ✅ Contrat se termine le {new Date(formData.contract_end_date).toLocaleDateString('fr-FR')}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

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

        {showReminderForm && (
          <ReminderForm
            leadId={lead?.id}
            onSave={handleAddReminder}
            onCancel={() => setShowReminderForm(false)}
          />
        )}
      </div>
    </div>
  );
};

const LeadsTable = ({ leads, onEdit, onDelete, onStatusChange, statusColors, config }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {/* Version Desktop - Table */}
      <div className="hidden lg:block overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Société</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contact</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Véhicules</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date création</th>
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
                    {lead.vehicles && lead.vehicles.length > 0 ? (
                      <>
                        <div>
                          {lead.vehicles[0].brand || 'Marque'} {lead.vehicles[0].model || (lead.vehicles[0].brand ? '(modèle à définir)' : 'non définie')}
                        </div>
                        <div className="text-sm text-gray-500">
                          {lead.vehicles[0].carburant ? `${lead.vehicles[0].carburant}` : 'Carburant à définir'}
                          {lead.vehicles[0].contract_duration && ` - ${lead.vehicles[0].contract_duration}mois`}
                          {lead.vehicles[0].tarif_mensuel && (
                            <span className="ml-2 text-green-600">{lead.vehicles[0].tarif_mensuel}</span>
                          )}
                          {lead.vehicles[0].commission_agence && (
                            <span className={`ml-2 text-xs px-2 py-1 rounded ${
                              lead.vehicles[0].payment_status === 'paye' 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-orange-100 text-orange-800'
                            }`}>
                              {lead.vehicles[0].payment_status === 'paye' ? '✓ Payé' : '⏳ Attente'}
                            </span>
                          )}
                        </div>
                        {lead.vehicles.length > 1 && (
                          <div className="text-xs text-blue-600">
                            +{lead.vehicles.length - 1} véhicule{lead.vehicles.length > 2 ? 's' : ''}
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="text-sm text-gray-400 italic">
                        <span className="inline-block w-4 h-4 text-center">🚗</span> À définir plus tard
                      </div>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <select
                    value={lead.status}
                    onChange={(e) => onStatusChange(lead.id, e.target.value)}
                    className="text-sm border-none bg-transparent focus:ring-2 focus:ring-blue-500 rounded"
                  >
                    <option value="a_contacter">🔴 À contacter</option>
                    <option value="premier_contact">Premier contact</option>
                    <option value="relance">Relance</option>
                    <option value="attribue">Attribué</option>
                    <option value="offre">Offre</option>
                    <option value="attente_document">Attente document</option>
                    <option value="etude_en_cours">Étude en cours</option>
                    <option value="accord">Accord</option>
                    <option value="livree">🟢 Livrée</option>
                    <option value="perdu">Perdu</option>
                  </select>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div className="font-medium">
                    {lead.lead_creation_date ? 
                      new Date(lead.lead_creation_date).toLocaleDateString('fr-FR') : 
                      'Non définie'
                    }
                  </div>
                  <div className="text-xs text-gray-500">
                    {lead.created_at ? 
                      `Système: ${new Date(lead.created_at).toLocaleDateString('fr-FR')}` : 
                      ''
                    }
                  </div>
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

      {/* Version Mobile - Cards */}
      <div className="lg:hidden">
        <div className="divide-y divide-gray-200">
          {leads.length > 0 ? (
            leads.map((lead) => (
              <div key={lead.id} className="p-4 space-y-3">
                {/* En-tête de la carte */}
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{lead.company.name}</h3>
                    <p className="text-sm text-gray-500">{lead.contact.first_name} {lead.contact.last_name}</p>
                  </div>
                  <div className="ml-4 flex space-x-2">
                    <button
                      onClick={() => onEdit(lead)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => onDelete(lead.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                    >
                      🗑️
                    </button>
                  </div>
                </div>

                {/* Statut */}
                <div className="flex items-center space-x-3">
                  <span className="text-sm font-medium text-gray-700">Statut:</span>
                  <select
                    value={lead.status}
                    onChange={(e) => onStatusChange(lead.id, e.target.value)}
                    className="text-sm border border-gray-300 rounded-md px-2 py-1 focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="a_contacter">🔴 À contacter</option>
                    <option value="premier_contact">Premier contact</option>
                    <option value="relance">Relance</option>
                    <option value="attribue">Attribué</option>
                    <option value="offre">Offre</option>
                    <option value="attente_document">Attente document</option>
                    <option value="etude_en_cours">Étude en cours</option>
                    <option value="accord">Accord</option>
                    <option value="livree">🟢 Livrée</option>
                    <option value="perdu">Perdu</option>
                  </select>
                </div>

                {/* Véhicule */}
                {lead.vehicles && lead.vehicles.length > 0 && (
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-gray-700 mb-1">🚗 Véhicule:</p>
                    <p className="text-sm text-gray-900">
                      {lead.vehicles[0].brand || 'Marque'} {lead.vehicles[0].model || 'Modèle'} 
                      {lead.vehicles[0].carburant && ` (${lead.vehicles[0].carburant})`}
                    </p>
                    {lead.vehicles[0].tarif_mensuel && (
                      <p className="text-sm text-green-600 mt-1">💰 {lead.vehicles[0].tarif_mensuel}</p>
                    )}
                    {lead.vehicles.length > 1 && (
                      <p className="text-xs text-blue-600 mt-1">+{lead.vehicles.length - 1} autre(s) véhicule(s)</p>
                    )}
                  </div>
                )}

                {/* Informations complémentaires */}
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <p className="text-gray-500">📅 Création:</p>
                    <p className="font-medium">
                      {lead.lead_creation_date ? 
                        new Date(lead.lead_creation_date).toLocaleDateString('fr-FR') : 
                        'Non définie'
                      }
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-500">👤 Commercial:</p>
                    <p className="font-medium">{lead.assigned_to_commercial || 'Non assigné'}</p>
                  </div>
                </div>

                {/* Contact */}
                <div className="pt-2 border-t border-gray-100">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-500">{lead.contact.email}</span>
                    <span className="text-gray-500">{lead.contact.phone}</span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl text-gray-300 mb-4">📋</div>
              <p>Aucun lead trouvé</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const LeadsView = ({ leads, config, onRefresh }) => {
  const [showForm, setShowForm] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState(''); // Nouveau état pour le tri

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
      lead.contact.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (lead.vehicles && lead.vehicles.some(v => 
        v.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
        v.model.toLowerCase().includes(searchTerm.toLowerCase())
      )) ||
      (lead.note && lead.note.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesStatus = !statusFilter || lead.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  // Fonction de tri
  const sortedLeads = [...filteredLeads].sort((a, b) => {
    if (!sortBy) return 0; // Pas de tri si aucun critère sélectionné
    
    switch (sortBy) {
      case 'company_name':
        return a.company.name.localeCompare(b.company.name);
      
      case 'contact_name':
        const nameA = `${a.contact.first_name} ${a.contact.last_name}`.toLowerCase();
        const nameB = `${b.contact.first_name} ${b.contact.last_name}`.toLowerCase();
        return nameA.localeCompare(nameB);
      
      case 'status':
        return a.status.localeCompare(b.status);
      
      case 'commercial':
        const commercialA = a.assigned_to_commercial || '';
        const commercialB = b.assigned_to_commercial || '';
        return commercialA.localeCompare(commercialB);
      
      case 'prestataire':
        const prestataireA = a.assigned_to_prestataire || '';
        const prestataireB = b.assigned_to_prestataire || '';
        return prestataireA.localeCompare(prestataireB);
      
      case 'vehicle_brand':
        const brandA = (a.vehicles && a.vehicles[0] ? a.vehicles[0].brand : '');
        const brandB = (b.vehicles && b.vehicles[0] ? b.vehicles[0].brand : '');
        return brandA.localeCompare(brandB);
      
      case 'created_at':
        const dateA = new Date(a.created_at || '');
        const dateB = new Date(b.created_at || '');
        return dateB - dateA; // Plus récent en premier
      
      case 'created_at_asc':
        const dateAAsc = new Date(a.created_at || '');
        const dateBAsc = new Date(b.created_at || '');
        return dateAAsc - dateBAsc; // Plus ancien en premier
      
      case 'lead_creation_date':
        const leadDateA = new Date(a.lead_creation_date || '');
        const leadDateB = new Date(b.lead_creation_date || '');
        return leadDateB - leadDateA; // Plus récent en premier
      
      case 'lead_creation_date_asc':
        const leadDateAAsc = new Date(a.lead_creation_date || '');
        const leadDateBAsc = new Date(b.lead_creation_date || '');
        return leadDateAAsc - leadDateBAsc; // Plus ancien en premier
      
      case 'commission_total':
        const getTotalCommission = (lead) => {
          return lead.vehicles?.reduce((total, vehicle) => {
            const commission = vehicle.commission_agence || '';
            const numbers = commission.match(/\d+/);
            return total + (numbers ? parseInt(numbers[0]) : 0);
          }, 0) || 0;
        };
        return getTotalCommission(b) - getTotalCommission(a); // Plus élevé en premier
      
      default:
        return 0;
    }
  });

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Gestion des Leads</h2>
          <p className="text-gray-600 mt-1">
            {sortedLeads.length} lead{sortedLeads.length > 1 ? 's' : ''} affiché{sortedLeads.length > 1 ? 's' : ''}
            {sortBy && (
              <span className="ml-2 text-blue-600 font-medium">
                • Trié par {
                  sortBy === 'company_name' ? 'nom de société' :
                  sortBy === 'contact_name' ? 'contact' :
                  sortBy === 'status' ? 'statut' :
                  sortBy === 'commercial' ? 'commercial' :
                  sortBy === 'prestataire' ? 'prestataire' :
                  sortBy === 'vehicle_brand' ? 'marque véhicule' :
                  sortBy === 'lead_creation_date' ? 'date création (récent)' :
                  sortBy === 'lead_creation_date_asc' ? 'date création (ancien)' :
                  sortBy === 'created_at' ? 'date système (récent)' :
                  sortBy === 'created_at_asc' ? 'date système (ancien)' :
                  sortBy === 'commission_total' ? 'commission' : sortBy
                }
              </span>
            )}
          </p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors font-medium"
        >
          ➕ Nouveau Lead
        </button>
      </div>

      <div className="flex flex-wrap gap-4 mb-6">
        <input
          type="text"
          placeholder="Rechercher..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 min-w-64 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Tous les statuts</option>
          <option value="a_contacter">À contacter</option>
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
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-gradient-to-r from-blue-50 to-blue-100"
        >
          <option value="">📊 Trier par...</option>
          <option value="company_name">🏢 Nom de société (A-Z)</option>
          <option value="contact_name">👤 Contact (A-Z)</option>
          <option value="status">📋 Statut (A-Z)</option>
          <option value="commercial">👥 Commercial (A-Z)</option>
          <option value="prestataire">🤝 Prestataire (A-Z)</option>
          <option value="vehicle_brand">🚗 Marque véhicule (A-Z)</option>
          <option value="lead_creation_date">📅 Date création (Plus récent)</option>
          <option value="lead_creation_date_asc">📅 Date création (Plus ancien)</option>
          <option value="created_at">🔧 Date système (Plus récent)</option>
          <option value="created_at_asc">🔧 Date système (Plus ancien)</option>
          <option value="commission_total">💰 Commission (Plus élevée)</option>
        </select>
      </div>

      <LeadsTable 
        leads={sortedLeads}
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

const Calendar = ({ leads }) => {
  const [upcomingReminders, setUpcomingReminders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchReminders = async () => {
    try {
      const response = await axios.get(`${API}/calendar/reminders?days=30`);
      setUpcomingReminders(response.data);
    } catch (error) {
      console.error('Error fetching reminders:', error);
    }
  };

  const handleDeleteReminder = async (reminderId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce rappel ?')) {
      try {
        setLoading(true);
        await axios.delete(`${API}/reminders/${reminderId}`);
        fetchReminders(); // Recharger la liste
        alert('Rappel supprimé avec succès !');
      } catch (error) {
        console.error('Error deleting reminder:', error);
        alert('Erreur lors de la suppression du rappel');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleToggleCompleted = async (reminderId) => {
    try {
      await axios.put(`${API}/reminders/${reminderId}/complete`);
      fetchReminders(); // Recharger la liste
    } catch (error) {
      console.error('Error updating reminder:', error);
      alert('Erreur lors de la mise à jour du rappel');
    }
  };

  useEffect(() => {
    fetchReminders();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Calendrier & Tâches</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-900">📅 Rappels programmés</h3>
          {loading && (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            </div>
          )}
          <div className="space-y-4">
            {upcomingReminders.length > 0 ? (
              upcomingReminders.map((reminder) => (
                <div key={reminder.id} className={`flex items-center space-x-4 p-4 rounded-lg border ${
                  reminder.completed ? 'bg-green-50 border-green-200' : 
                  reminder.priority === 'urgent' ? 'bg-red-50 border-red-200' :
                  reminder.priority === 'high' ? 'bg-orange-50 border-orange-200' :
                  'bg-blue-50 border-blue-200'
                }`}>
                  <div className={`w-3 h-3 rounded-full ${
                    reminder.completed ? 'bg-green-500' : 
                    reminder.priority === 'urgent' ? 'bg-red-500' :
                    reminder.priority === 'high' ? 'bg-orange-500' :
                    'bg-blue-500'
                  }`}></div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <p className={`font-medium ${
                        reminder.completed ? 'text-green-900 line-through' : 'text-gray-900'
                      }`}>
                        {reminder.title}
                      </p>
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        reminder.priority === 'urgent' ? 'bg-red-100 text-red-800' :
                        reminder.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                        reminder.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {reminder.priority === 'urgent' ? '🚨 Urgent' :
                         reminder.priority === 'high' ? '⚡ Prioritaire' :
                         reminder.priority === 'medium' ? '📋 Normal' : '📝 Faible'}
                      </span>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        reminder.reminder_type === 'call' ? 'bg-blue-100 text-blue-800' :
                        reminder.reminder_type === 'email' ? 'bg-purple-100 text-purple-800' :
                        reminder.reminder_type === 'meeting' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {reminder.reminder_type === 'call' ? '📞 Appel' :
                         reminder.reminder_type === 'email' ? '✉️ Email' :
                         reminder.reminder_type === 'meeting' ? '🤝 RDV' :
                         reminder.reminder_type === 'follow_up' ? '📋 Suivi' : '📝 Général'}
                      </span>
                    </div>
                    {reminder.description && (
                      <p className={`text-sm ${
                        reminder.completed ? 'text-green-600' : 'text-gray-600'
                      } mt-1`}>
                        {reminder.description}
                      </p>
                    )}
                    <p className={`text-xs ${
                      reminder.completed ? 'text-green-500' : 'text-gray-500'
                    } mt-1`}>
                      📅 {new Date(reminder.reminder_date).toLocaleString('fr-FR')}
                      {reminder.completed && reminder.completed_at && (
                        <span className="ml-2">• ✅ Terminé le {new Date(reminder.completed_at).toLocaleDateString('fr-FR')}</span>
                      )}
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleToggleCompleted(reminder.id)}
                      className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                        reminder.completed 
                          ? 'bg-orange-600 text-white hover:bg-orange-700' 
                          : 'bg-green-600 text-white hover:bg-green-700'
                      }`}
                      disabled={loading}
                    >
                      {reminder.completed ? '↶ Rouvrir' : '✓ Terminé'}
                    </button>
                    <button
                      onClick={() => handleDeleteReminder(reminder.id)}
                      className="px-3 py-1 bg-red-600 text-white rounded text-xs font-medium hover:bg-red-700 transition-colors"
                      disabled={loading}
                    >
                      🗑️ Supprimer
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500">Aucun rappel programmé</p>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-900">📋 Tâches suggérées</h3>
          <div className="space-y-4">
            {leads.slice(0, 5).map((lead) => (
              <div key={lead.id} className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
                <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                <div>
                  <p className="font-medium">Relancer {lead.contact.first_name} {lead.contact.last_name}</p>
                  <p className="text-sm text-gray-600">
                    {lead.company.name} - {lead.vehicles && lead.vehicles[0] ? `${lead.vehicles[0].brand} ${lead.vehicles[0].model}` : 'Véhicule à définir'}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const Backup = () => {
  const [backupStatus, setBackupStatus] = useState({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const fetchBackupStatus = async () => {
    try {
      const response = await axios.get(`${API}/backup/status`);
      setBackupStatus(response.data);
    } catch (error) {
      console.error('Error fetching backup status:', error);
    }
  };

  const handleExport = async () => {
    try {
      setLoading(true);
      setMessage('');
      const response = await axios.get(`${API}/backup/export`);
      
      // Télécharger le fichier JSON
      const dataStr = JSON.stringify(response.data.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      
      const now = new Date();
      const timestamp = now.toISOString().slice(0, 19).replace(/:/g, '-');
      link.download = `CRM_BACKUP_${timestamp}.json`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      setMessage(`✅ ${response.data.message}`);
      fetchBackupStatus();
    } catch (error) {
      setMessage(`❌ Erreur export: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setLoading(true);
      setMessage('');
      
      const text = await file.text();
      const backupData = JSON.parse(text);
      
      if (window.confirm('⚠️ ATTENTION: Cette opération va remplacer TOUTES vos données actuelles. Êtes-vous sûr ?')) {
        const response = await axios.post(`${API}/backup/import`, backupData);
        setMessage(`✅ ${response.data.message}`);
        fetchBackupStatus();
        
        // Recharger la page pour afficher les nouvelles données
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      }
    } catch (error) {
      setMessage(`❌ Erreur import: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
      event.target.value = ''; // Reset file input
    }
  };

  useEffect(() => {
    fetchBackupStatus();
  }, []);

  return (
    <div className="p-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">💾 Gestion des Sauvegardes</h2>
        <p className="text-gray-600">Sauvegardez et restaurez vos données CRM</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${message.includes('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
          {message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Statut des sauvegardes */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-900">📊 Statut des Sauvegardes</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
              <span className="font-medium">Leads en mémoire:</span>
              <span className="text-blue-600 font-bold">{backupStatus.leads_count || 0}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
              <span className="font-medium">Rappels en mémoire:</span>
              <span className="text-green-600 font-bold">{backupStatus.reminders_count || 0}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-yellow-50 rounded-lg">
              <span className="font-medium">Sauvegarde leads:</span>
              <span className={backupStatus.leads_backup_exists ? 'text-green-600' : 'text-red-600'}>
                {backupStatus.leads_backup_exists ? '✅ Existe' : '❌ Absent'}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
              <span className="font-medium">Sauvegarde rappels:</span>
              <span className={backupStatus.reminders_backup_exists ? 'text-green-600' : 'text-red-600'}>
                {backupStatus.reminders_backup_exists ? '✅ Existe' : '❌ Absent'}
              </span>
            </div>
            {backupStatus.leads_backup_modified && (
              <div className="p-3 bg-gray-50 rounded-lg text-sm">
                <span className="font-medium">Dernière sauvegarde:</span><br/>
                {new Date(backupStatus.leads_backup_modified).toLocaleString('fr-FR')}
              </div>
            )}
          </div>
        </div>

        {/* Actions de sauvegarde */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-900">⚡ Actions</h3>
          <div className="space-y-4">
            <button
              onClick={handleExport}
              disabled={loading}
              className="w-full bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors font-medium disabled:opacity-50"
            >
              {loading ? '⏳ Export en cours...' : '📥 Exporter toutes les données'}
            </button>
            
            <div className="relative">
              <input
                type="file"
                accept=".json"
                onChange={handleImport}
                disabled={loading}
                className="hidden"
                id="import-file"
              />
              <label
                htmlFor="import-file"
                className={`w-full bg-green-600 text-white px-6 py-3 rounded-md hover:bg-green-700 transition-colors font-medium cursor-pointer block text-center ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? '⏳ Import en cours...' : '📤 Importer des données'}
              </label>
            </div>

            <button
              onClick={fetchBackupStatus}
              className="w-full bg-gray-600 text-white px-6 py-3 rounded-md hover:bg-gray-700 transition-colors font-medium"
            >
              🔄 Actualiser le statut
            </button>
          </div>

          <div className="mt-6 p-4 bg-amber-50 rounded-lg">
            <h4 className="font-medium text-amber-800 mb-2">💡 Information:</h4>
            <ul className="text-sm text-amber-700 space-y-1">
              <li>• Sauvegarde automatique à chaque modification</li>
              <li>• Restauration automatique au démarrage</li>
              <li>• Export: fichier JSON téléchargeable</li>
              <li>• Import: remplace toutes les données</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

// Clients Component
const Clients = ({ config }) => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('');

  const fetchClients = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  // Filtrage et tri des clients
  const filteredClients = clients.filter(client => {
    const matchesSearch = !searchTerm || 
      client.company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      client.contact.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      client.contact.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (client.vehicles && client.vehicles.some(v => 
        v.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
        v.model.toLowerCase().includes(searchTerm.toLowerCase())
      ));
    return matchesSearch;
  });

  const sortedClients = [...filteredClients].sort((a, b) => {
    if (!sortBy) return 0;
    
    switch (sortBy) {
      case 'company_name':
        return a.company.name.localeCompare(b.company.name);
      case 'delivery_date':
        const dateA = new Date(a.delivery_date || '');
        const dateB = new Date(b.delivery_date || '');
        return dateB - dateA;
      case 'contract_end_date':
        const endDateA = new Date(a.contract_end_date || '');
        const endDateB = new Date(b.contract_end_date || '');
        return endDateA - endDateB;
      case 'commission_total':
        const getTotalCommission = (client) => {
          return client.vehicles?.reduce((total, vehicle) => {
            const commission = vehicle.commission_agence || '';
            const numbers = commission.match(/\d+/);
            return total + (numbers ? parseInt(numbers[0]) : 0);
          }, 0) || 0;
        };
        return getTotalCommission(b) - getTotalCommission(a);
      default:
        return 0;
    }
  });

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-green-900">🎯 Clients (Livrés)</h2>
          <p className="text-green-600 mt-1">
            {sortedClients.length} client{sortedClients.length > 1 ? 's' : ''} livré{sortedClients.length > 1 ? 's' : ''}
            {sortBy && (
              <span className="ml-2 text-green-700 font-medium">
                • Trié par {
                  sortBy === 'company_name' ? 'nom société' :
                  sortBy === 'delivery_date' ? 'date livraison' :
                  sortBy === 'contract_end_date' ? 'fin contrat' :
                  sortBy === 'commission_total' ? 'commission' : sortBy
                }
              </span>
            )}
          </p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-green-700">
            ✅ Affaires finalisées et véhicules livrés
          </p>
        </div>
      </div>

      {/* Filtres et tri */}
      <div className="flex flex-wrap gap-4 mb-6">
        <input
          type="text"
          placeholder="Rechercher un client..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 min-w-64 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500"
        />
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 bg-gradient-to-r from-green-50 to-green-100"
        >
          <option value="">📊 Trier par...</option>
          <option value="company_name">🏢 Nom société (A-Z)</option>
          <option value="delivery_date">📅 Date livraison (Plus récent)</option>
          <option value="contract_end_date">⏰ Fin contrat (Plus proche)</option>
          <option value="commission_total">💰 Commission (Plus élevée)</option>
        </select>
      </div>

      {/* Table des clients */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-green-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-green-800 uppercase tracking-wider">Client</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-green-800 uppercase tracking-wider">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-green-800 uppercase tracking-wider">Véhicule livré</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-green-800 uppercase tracking-wider">Livraison</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-green-800 uppercase tracking-wider">Fin contrat</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-green-800 uppercase tracking-wider">Commission</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sortedClients.length > 0 ? (
                sortedClients.map((client) => (
                  <tr key={client.id} className="hover:bg-green-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{client.company.name}</div>
                        <div className="text-sm text-gray-500">{client.company.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {client.contact.first_name} {client.contact.last_name}
                        </div>
                        <div className="text-sm text-gray-500">{client.contact.phone}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {client.vehicles && client.vehicles.length > 0 ? (
                          <>
                            <div className="font-medium">
                              {client.vehicles[0].brand} {client.vehicles[0].model}
                            </div>
                            <div className="text-sm text-gray-500">
                              {client.vehicles[0].carburant}
                              {client.vehicles[0].tarif_mensuel && (
                                <span className="ml-2 text-green-600">{client.vehicles[0].tarif_mensuel}</span>
                              )}
                            </div>
                          </>
                        ) : (
                          <span className="text-gray-400">Véhicule non spécifié</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="font-medium text-green-700">
                        {client.delivery_date ? 
                          new Date(client.delivery_date).toLocaleDateString('fr-FR') : 
                          'Non définie'
                        }
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>
                        {client.contract_end_date ? 
                          new Date(client.contract_end_date).toLocaleDateString('fr-FR') : 
                          'Non calculée'
                        }
                      </div>
                      {client.contract_end_date && (
                        <div className="text-xs text-gray-500">
                          {Math.ceil((new Date(client.contract_end_date) - new Date()) / (1000 * 60 * 60 * 24))} jours restants
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {client.vehicles && client.vehicles[0]?.commission_agence ? (
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {client.vehicles[0].commission_agence}
                          </div>
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            client.vehicles[0].payment_status === 'paye' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-orange-100 text-orange-800'
                          }`}>
                            {client.vehicles[0].payment_status === 'paye' ? '✅ Payé' : '⏳ En attente'}
                          </span>
                        </div>
                      ) : (
                        <span className="text-gray-400">Non définie</span>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                    <div className="text-4xl text-gray-300 mb-4">🎯</div>
                    <p className="text-lg font-medium">Aucun client livré pour le moment</p>
                    <p className="text-sm">Les leads avec le statut "Livrée" apparaîtront ici</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

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
        axios.get(`${API}/leads/active`), // Seuls les leads actifs (non livrés)
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
          <p className="text-gray-600">Chargement de CRM LEASINPROFESSIONNEL.FR...</p>
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
        {activeTab === 'clients' && (
          <Clients config={config} />
        )}
        {activeTab === 'calendar' && (
          <Calendar leads={leads} />
        )}
        {activeTab === 'backup' && (
          <Backup />
        )}
      </main>
    </div>
  );
}

export default App;