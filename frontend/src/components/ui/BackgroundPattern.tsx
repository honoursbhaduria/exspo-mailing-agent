import React from 'react';
import styled from 'styled-components';

export const BackgroundPattern: React.FC = () => {
  return (
    <StyledWrapper>
      <div className="ambient-glow" />
      <div className="grid-overlay" />
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  z-index: -10;
  pointer-events: none;
  overflow: hidden;
  background-color: #F8FAFC;

  .ambient-glow {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(
      circle at 50% 0%,
      rgba(186, 230, 253, 0.45) 0%,
      rgba(224, 242, 254, 0.2) 45%,
      rgba(248, 250, 252, 0) 75%
    );
  }

  .grid-overlay {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(to right, rgba(203, 213, 225, 0.45) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(203, 213, 225, 0.45) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0) 80%);
    -webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0) 80%);
  }
`;

export default BackgroundPattern;
