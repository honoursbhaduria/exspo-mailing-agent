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
  button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 48px;
    padding: 0 24px;
    border-radius: 12px;
    border: 1.5px solid ${({ $variant }) => ($variant === 'primary' ? '#7DD3FC' : '#CBD5E1')};
    background: ${({ $variant }) => ($variant === 'primary' ? '#BAE6FD' : '#FFFFFF')};
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease-in;
    z-index: 1;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.1);
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

  button:hover::before,
  button:hover::after {
    width: 58%;
  }

  button span {
    color: #000000;
    font-size: 0.92rem;
    font-weight: 800;
    letter-spacing: -0.2px;
    transition: all 0.2s ease-in;
    display: flex;
    align-items: center;
    gap: 8px;
  }
`;

export default SlideHoverButton;
