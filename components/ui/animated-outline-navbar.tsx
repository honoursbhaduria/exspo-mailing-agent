import React, { useState } from 'react';
import styled from 'styled-components';

interface AnimatedOutlineNavbarProps {
  items?: string[];
  activeIndex?: number;
  onSelect?: (index: number) => void;
}

export const AnimatedOutlineNavbar: React.FC<AnimatedOutlineNavbarProps> = ({
  items = ['Home', 'Contact', 'About', 'FAQ'],
  activeIndex = 0,
  onSelect,
}) => {
  return (
    <StyledWrapper>
      <div className="nav">
        <div className="container">
          {items.map((item, idx) => (
            <div
              key={item}
              className={`btn ${idx === activeIndex ? 'active' : ''}`}
              onClick={() => onSelect && onSelect(idx)}
            >
              {item}
            </div>
          ))}
          <svg className="outline" overflow="visible" width={400} height={60} viewBox="0 0 400 60" xmlns="http://www.w3.org/2000/svg">
            <rect className="rect" pathLength={100} x={0} y={0} width={400} height={60} fill="transparent" strokeWidth={4} />
          </svg>
        </div>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  .outline {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .rect {
    stroke-dashoffset: 5;
    stroke-dasharray: 0 0 10 40 10 40;
    transition: 0.5s;
    stroke: #03045e;
  }

  .nav {
    position: relative;
    width: 460px;
    height: 52px;
    margin: 0 auto;
  }

  .container:hover .outline .rect {
    transition: 999999s;
    stroke-dashoffset: 1;
    stroke-dasharray: 0;
  }

  .container {
    position: absolute;
    inset: 0;
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #ECEFF8;
    box-shadow: 0 4px 16px rgba(3, 4, 94, 0.04);
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    padding: 0.4em;
  }

  .btn {
    padding: 0.4em 1.2em;
    color: #03045e;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: 8px;
    transition: 0.15s;
  }

  .btn:hover, .btn.active {
    background: #F1F4FA;
    color: #240046;
  }

  .btn:nth-child(1):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 2 8 73.3 8 10.7;
  }

  .btn:nth-child(2):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 12.6 9.5 49.3 9.5 31.6;
  }

  .btn:nth-child(3):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 24.5 8.5 27.5 8.5 55.5;
  }

  .btn:nth-child(4):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 34.7 6.9 10.2 6.9 76;
  }

  .btn:hover ~ .outline .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 0 10 40 10 40;
    transition: 0.5s !important;
  }
`;

export default AnimatedOutlineNavbar;
