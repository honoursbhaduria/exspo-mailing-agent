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

  .container {
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to bottom,
        #fff 0%,
        #fff 40%,
        rgba(255, 255, 255, 0) 100%
      ),
      linear-gradient(to right, #0ed2da, #5f29c7);
    position: relative;
    overflow: hidden;
    filter: blur(0.5px);
  }

  .container::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: linear-gradient(90deg, #ccc 1px, transparent 1px);
    background-size: 50px 100%;
    pointer-events: none;
    mask-image: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 1) 0%,
      rgba(0, 0, 0, 0) 70%
    );
    -webkit-mask-image: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 1) 0%,
      rgba(0, 0, 0, 0) 70%
    );
  }

  .container::after {
    content: "";
    position: absolute;
    inset: 0;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    pointer-events: none;
  }
`;

export default BackgroundPattern;
