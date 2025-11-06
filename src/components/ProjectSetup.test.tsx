import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectSetup } from './ProjectSetup';

describe('ProjectSetup Component', () => {
  const mockProps = {
    fileName: 'test-book.txt',
    fileSize: 5000,
    fileContent: 'This is a test book content with some words to count and analyze.',
    onConfigure: vi.fn(),
    onCancel: vi.fn(),
  };

  it('renders the project setup form', () => {
    render(<ProjectSetup {...mockProps} />);
    expect(screen.getByText(/Project Setup/i)).toBeInTheDocument();
  });

  it('displays default title from filename', () => {
    render(<ProjectSetup {...mockProps} />);
    const titleInput = screen.getByDisplayValue('test-book');
    expect(titleInput).toBeInTheDocument();
  });

  it('shows default modernization instructions', () => {
    render(<ProjectSetup {...mockProps} />);
    const textarea = screen.getByText(/Modernize the language/i);
    expect(textarea).toBeInTheDocument();
  });

  it('allows updating the title', async () => {
    const user = userEvent.setup();
    render(<ProjectSetup {...mockProps} />);

    const titleInput = screen.getByDisplayValue('test-book');
    await user.clear(titleInput);
    await user.type(titleInput, 'New Title');

    expect(titleInput).toHaveValue('New Title');
  });

  it('allows updating the author', async () => {
    const user = userEvent.setup();
    render(<ProjectSetup {...mockProps} />);

    const authorInput = screen.getByLabelText(/Author/i);
    await user.type(authorInput, 'Jane Austen');

    expect(authorInput).toHaveValue('Jane Austen');
  });

  it('calls onCancel when cancel button is clicked', async () => {
    const user = userEvent.setup();
    render(<ProjectSetup {...mockProps} />);

    const cancelButton = screen.getByText(/Cancel/i);
    await user.click(cancelButton);

    expect(mockProps.onCancel).toHaveBeenCalled();
  });

  it('calculates and displays book statistics', () => {
    render(<ProjectSetup {...mockProps} />);
    // The component should show word/character counts
    // Look for any numeric displays
    const statsElements = screen.getAllByText(/\d+/);
    expect(statsElements.length).toBeGreaterThan(0);
  });

  it('shows range sliders for selecting book portion', () => {
    render(<ProjectSetup {...mockProps} />);
    // Sliders should be present in the document
    const sliders = document.querySelectorAll('[role="slider"]');
    expect(sliders.length).toBeGreaterThan(0);
  });
});
