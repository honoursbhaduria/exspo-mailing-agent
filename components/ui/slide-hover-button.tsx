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
  /* From uiverse.io by @Ali-Tahmazi99 */
  button {
    display: inline-block;
    min-width: 150px;
    height: 50px;
    padding: 0 24px;
    border-radius: 10px;
    border: 1px solid #03045e;
    background: #ffffff;
    position: relative;
    overflow: hidden;
    transition: all 0.5s ease-in;
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
    transition: all 0.5s;
    overflow: hidden;
    z-index: -1;
  }

  button::before {
    left: -10px;
    background: #240046;
  }

  button::after {
    right: -10px;
    background: #5a189a;
  }

  button:hover::before,
  button:hover::after {
    width: 58%;
  }

  button:hover span {
    color: #e0aaff;
    transition: 0.3s;
  }

  button span {
    color: #03045e;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease-in;
  }
`;

export default SlideHoverButton;
