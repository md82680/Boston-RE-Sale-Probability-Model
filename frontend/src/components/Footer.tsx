import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white mt-12 py-6 border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-gray-500">
          © {new Date().getFullYear()} Real Estate Sale Probability Predictor
        </p>
        <p className="text-center text-xs text-gray-400 mt-1">
          Powered by Machine Learning
        </p>
      </div>
    </footer>
  );
};

export default Footer;

