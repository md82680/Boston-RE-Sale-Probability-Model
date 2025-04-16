export interface Property {
  years_owned: number;
  has_liens: boolean;
  property_value: number;
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
