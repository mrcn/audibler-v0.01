import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

describe('Modern Audiobook Builder App', () => {
  it('renders the application', () => {
    render(<App />);
    expect(document.querySelector('.min-h-screen')).toBeInTheDocument();
  });

  it('displays the library view by default', () => {
    render(<App />);
    // Check if sample books are displayed
    expect(screen.getByText(/Pride and Prejudice/i)).toBeInTheDocument();
    expect(screen.getByText(/Moby-Dick/i)).toBeInTheDocument();
    expect(screen.getByText(/Sherlock Holmes/i)).toBeInTheDocument();
    expect(screen.getByText(/Frankenstein/i)).toBeInTheDocument();
  });

  it('has navigation functionality in header', () => {
    render(<App />);
    // The header component should be rendered
    const header = document.querySelector('header') || document.querySelector('nav');
    expect(header).toBeTruthy();
  });

  it('shows upload button in library view', async () => {
    render(<App />);
    const uploadButtons = screen.queryAllByText(/upload/i);
    expect(uploadButtons.length).toBeGreaterThan(0);
  });

  it('displays book metadata correctly', () => {
    render(<App />);
    // Check for authors
    expect(screen.getByText(/Jane Austen/i)).toBeInTheDocument();
    expect(screen.getByText(/Herman Melville/i)).toBeInTheDocument();
  });

  it('shows different book statuses', () => {
    render(<App />);
    // The app should render books with different statuses
    // We can check if the status indicators are present by checking the DOM structure
    const bookCards = document.querySelectorAll('[class*="book"]');
    expect(bookCards.length).toBeGreaterThan(0);
  });
});
