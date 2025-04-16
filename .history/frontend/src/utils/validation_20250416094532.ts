import { Property } from '../types';

export const validatePropertyData = (property: Property): Record<string, string> => {
  const errors: Record<string, string> = {};

  // Years owned validation
  if (property.years_owned < 0) {
    errors.years_owned = 'Years owned cannot be negative';
  }
  if (!property.years_owned && property.years_owned !== 0) {
    errors.years_owned = 'Years owned is required';
  }

  // Property value validation
  if (property.property_value <= 0) {
    errors.property_value = 'Property value must be greater than 0';
  }
  if (!property.property_value) {
    errors.property_value = 'Property value is required';
  }

  // Last transaction date validation
  if (!property.last_transaction_date) {
    errors.last_transaction_date = 'Last transaction date is required';
  }
  const transactionDate = new Date(property.last_transaction_date);
  if (transactionDate > new Date()) {
    errors.last_transaction_date = 'Last transaction date cannot be in the future';
  }

  // has_liens is a boolean and doesn't need validation

  return errors;
};
