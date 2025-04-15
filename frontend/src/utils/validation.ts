import { Property } from '../types';

export function validatePropertyData(property: Property): Record<string, string> {
  const errors: Record<string, string> = {};

  // Property value validation
  if (!property.property_value || property.property_value <= 0) {
    errors.property_value = 'Property value must be greater than 0';
  }

  // Square feet validation
  if (!property.square_feet || property.square_feet <= 0) {
    errors.square_feet = 'Square feet must be greater than 0';
  }

  // Bedrooms validation
  if (property.bedrooms < 0 || !Number.isInteger(property.bedrooms)) {
    errors.bedrooms = 'Bedrooms must be a positive integer';
  }

  // Bathrooms validation
  if (property.bathrooms < 0) {
    errors.bathrooms = 'Bathrooms must be a positive number';
  }

  // Property age validation
  if (property.property_age < 0) {
    errors.property_age = 'Property age must be a positive number';
  }

  // School rating validation
  if (property.school_rating < 0 || property.school_rating > 10) {
    errors.school_rating = 'School rating must be between 0 and 10';
  }

  // Mortgage rate validation
  if (property.mortgage_rate < 0) {
    errors.mortgage_rate = 'Mortgage rate must be a positive number';
  }

  // Years owned validation
  if (property.years_owned < 0) {
    errors.years_owned = 'Years owned must be a positive number';
  }

  return errors;
}
