import React from 'react';
import styled from 'styled-components';

export const BackgroundPattern: React.FC = () => {
  return (
    <StyledWrapper>
      <div className="container" />
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: -10;
  pointer-events: none;
  overflow: hidden;
  background-color: #F8FAFC;

  .container {
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to bottom,
        #ffffff 0%,
        #ffffff 45%,
        rgba(255, 255, 255, 0.85) 75%,
        rgba(255, 255, 255, 0.65) 100%
      ),
      linear-gradient(to right, rgba(14, 210, 218, 0.4), rgba(95, 41, 199, 0.35));
    position: relative;
    overflow: hidden;
  }

  .container::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: linear-gradient(90deg, #CBD5E1 1px, transparent 1px);
    background-size: 50px 100%;
    pointer-events: none;
    mask-image: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.8) 0%,
      rgba(0, 0, 0, 0) 70%
    );
    -webkit-mask-image: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.8) 0%,
      rgba(0, 0, 0, 0) 70%
    );
  }

  .container::after {
    content: "";
    position: absolute;
    inset: 0;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    pointer-events: none;
  }
`;

export default BackgroundPattern;
