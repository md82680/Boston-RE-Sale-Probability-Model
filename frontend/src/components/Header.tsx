import React from 'react';

const Header = () => {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Real Estate Sale Probability Predictor
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Predict the likelihood of a property selling based on its features
        </p>
      </div>
    </header>
  );
};

export default Header;
