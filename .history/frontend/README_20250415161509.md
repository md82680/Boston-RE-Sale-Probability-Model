# Boston Real Estate Sale Probability Predictor Frontend

## Overview
React-based frontend interface for the Real Estate Sale Probability Predictor. Provides user-friendly tools for both individual and batch property predictions.

## Features
- Single property prediction interface
- Batch upload functionality for multiple properties (CSV)
- Real-time prediction results
- Downloadable prediction reports
- Responsive design with Tailwind CSS

## Tech Stack
- React 18
- TypeScript
- Tailwind CSS
- Headless UI
- Hero Icons

## Installation

### Prerequisites
- Node.js (v16+)
- npm

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Project Structure
```
├── public/
├── src/
│   ├── components/     # React components
│   ├── services/       # API services
│   ├── types/         # TypeScript types
│   ├── utils/         # Utility functions
│   ├── App.tsx        # Root component
│   └── index.tsx      # Entry point
├── package.json
├── tsconfig.json
└── README.md
```

## Usage
The frontend will be available at http://localhost:3000 when running in development mode. Ensure the backend API is running for full functionality.

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
