import React from 'react';
import styled from 'styled-components';

interface SlideHoverButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children?: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

export const SlideHoverButton: React.FC<SlideHoverButtonProps> = ({
  children = 'Button',
  variant = 'primary',
  ...props
}) => {
  return (
    <StyledWrapper $variant={variant}>
      <button {...props}>
        <span>{children}</span>
      </button>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div<{ $variant: 'primary' | 'secondary' }>`
  width: 100%;

  button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 44px;
    padding: 0 16px;
    border-radius: 12px;
    border: 1.5px solid ${({ $variant }) => ($variant === 'primary' ? '#7DD3FC' : '#CBD5E1')};
    background: ${({ $variant }) => ($variant === 'primary' ? '#BAE6FD' : '#FFFFFF')};
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease-in-out;
    z-index: 1;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);
    -webkit-tap-highlight-color: transparent;

    @media (min-width: 640px) {
      min-height: 48px;
      padding: 0 24px;
    }
  }

  button:active:not(:disabled) {
    transform: scale(0.98);
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    box-shadow: none;
  }

  button::before,
  button::after {
    content: '';
    position: absolute;
    top: 0;
    width: 0;
    height: 100%;
    transform: skew(15deg);
    transition: all 0.4s ease;
    overflow: hidden;
    z-index: -1;
  }

  button::before {
    left: -10px;
    background: ${({ $variant }) => ($variant === 'primary' ? '#93C5FD' : '#F1F5F9')};
  }

  button::after {
    right: -10px;
    background: ${({ $variant }) => ($variant === 'primary' ? '#60A5FA' : '#E2E8F0')};
  }

  button:hover:not(:disabled)::before,
  button:hover:not(:disabled)::after {
    width: 58%;
  }

  button span {
    color: #000000;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: -0.2px;
    transition: all 0.2s ease-in;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 8px;

    @media (min-width: 640px) {
      font-size: 0.92rem;
    }
  }
`;

export default SlideHoverButton;
