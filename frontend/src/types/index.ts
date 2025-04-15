export interface Property {
  years_owned: number;
  property_value: number;
  square_feet: number;
  bedrooms: number;
  bathrooms: number;
  property_age: number;
  neighborhood: string;
  distance_to_t: number;
  school_rating: number;
  property_tax: number;
  has_liens: boolean;
  lien_amount: number;
  mortgage_rate: number;
  income_to_mortgage_ratio: number;
  market_inventory_months: number;
  avg_days_on_market: number;
  last_transaction_date: string;
}

export interface PredictionResponse {
  sale_probability: number;
  prediction_date: string;
  model_version: string;
}

export interface BatchPropertyRequest {
  properties: Property[];
}

export interface BatchPredictionResponse {
  predictions: number[];
  prediction_date: string;
  model_version: string;
}
