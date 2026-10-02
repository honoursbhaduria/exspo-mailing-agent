import React from 'react';
import styled from 'styled-components';

export const BackgroundPattern: React.FC = () => {
  return (
    <StyledWrapper>
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

  .grid-overlay {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(to right, #E2E8F0 1px, transparent 1px),
      linear-gradient(to bottom, #E2E8F0 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.7;
  }
`;

export default BackgroundPattern;
