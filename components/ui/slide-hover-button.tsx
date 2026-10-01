import React from 'react';
import styled from 'styled-components';

interface SlideHoverButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children?: React.ReactNode;
}

export const SlideHoverButton: React.FC<SlideHoverButtonProps> = ({ children = 'Button', ...props }) => {
  return (
    <StyledWrapper>
      <button {...props}>
        <span>{children}</span>
      </button>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  button {
    display: inline-block;
    min-width: 150px;
    height: 48px;
    padding: 0 24px;
    border-radius: 12px;
    border: 1.5px solid #7DD3FC;
    background: #BAE6FD;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease-in;
    z-index: 1;
    cursor: pointer;
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
    background: #93C5FD;
  }

  button::after {
    right: -10px;
    background: #60A5FA;
  }

  button:hover::before,
  button:hover::after {
    width: 58%;
  }

  button:hover span {
    color: #000000;
    transition: 0.3s;
  }

  button span {
    color: #000000;
    font-size: 16px;
    font-weight: 800;
    transition: all 0.3s ease-in;
  }
`;

export default SlideHoverButton;
