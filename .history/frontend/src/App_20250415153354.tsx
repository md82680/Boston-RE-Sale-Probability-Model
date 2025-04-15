import React, { useState, useEffect } from 'react';
import { checkHealth } from './services/api';
import Header from './components/Header';
import PropertyForm from './components/PropertyForm';
import BatchUpload from './components/BatchUpload';
import Footer from './components/Footer';

const App = () => {
  const [activeTab, setActiveTab] = useState('single' as 'single' | 'batch');
  const [apiStatus, setApiStatus] = useState('loading' as 'loading' | 'online' | 'offline');

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        await checkHealth();
        setApiStatus('online');
      } catch (error) {
        setApiStatus('offline');
        console.error('API health check failed:', error);
      }
    };

    checkApiStatus();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      
      <main className="container mx-auto py-8 px-4">
        {apiStatus === 'loading' && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Connecting to API...</p>
          </div>
        )}
        
        {apiStatus === 'offline' && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-8">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">API Offline</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>The prediction API appears to be offline. Please ensure the API server is running.</p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {apiStatus === 'online' && (
          <>
            <div className="flex border-b border-gray-200 mb-8">
              <button
                className={`px-4 py-2 text-sm font-medium ${
                  activeTab === 'single'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
                onClick={() => setActiveTab('single')}
              >
                Single Property
              </button>
              <button
                className={`ml-8 px-4 py-2 text-sm font-medium ${
                  activeTab === 'batch'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
                onClick={() => setActiveTab('batch')}
              >
                Batch Upload
              </button>
            </div>
            
            {activeTab === 'single' ? <PropertyForm /> : <BatchUpload />}
          </>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default App;

