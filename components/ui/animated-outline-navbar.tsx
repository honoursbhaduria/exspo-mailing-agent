import React, { useState } from 'react';
import styled from 'styled-components';

interface AnimatedOutlineNavbarProps {
  items?: string[];
  activeIndex?: number;
  onSelect?: (index: number) => void;
}

export const AnimatedOutlineNavbar: React.FC<AnimatedOutlineNavbarProps> = ({
  items = [
    'Discovered Records',
    'Classification Engine',
    'Profile Context & Themes',
    'AI Personalization',
    'Outreach Audit Log',
  ],
  activeIndex = 0,
  onSelect,
}) => {
  const [active, setActive] = useState(activeIndex);

  const handleClick = (idx: number) => {
    setActive(idx);
    if (onSelect) onSelect(idx);
  };

  return (
    <StyledWrapper>
      <div className="nav">
        <div className="container">
          {items.map((item, idx) => (
            <div
              key={item}
              className={`btn ${idx === active ? 'active' : ''}`}
              onClick={() => handleClick(idx)}
            >
              {item}
            </div>
          ))}
          <svg className="outline" overflow="visible" width={820} height={56} viewBox="0 0 820 56" xmlns="http://www.w3.org/2000/svg">
            <rect className="rect" pathLength={100} x={0} y={0} width={820} height={56} fill="transparent" strokeWidth={4} />
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
    stroke: #0284c7;
  }

  .nav {
    position: relative;
    width: 820px;
    height: 56px;
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
    background: #bef6; /* Ice-cyan light tint */
    border-radius: 14px;
    border: 1.5px solid #BAE6FD;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    padding: 0.4em 0.8em;
  }

  .btn {
    padding: 0.5em 1.2em;
    color: #000000;
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    border-radius: 10px;
    transition: 0.15s ease;
    user-select: none;
  }

  .btn:hover {
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .btn.active {
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12);
    border: 1.5px solid #BAE6FD;
  }

  .btn:nth-child(1):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 1.5 6 78 6 8.5;
  }

  .btn:nth-child(2):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 11 7 58 7 17;
  }

  .btn:nth-child(3):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 21 8 38 8 25;
  }

  .btn:nth-child(4):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 31 7 24 7 31;
  }

  .btn:nth-child(5):hover ~ svg .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 41 6 12 6 35;
  }

  .btn:hover ~ .outline .rect {
    stroke-dashoffset: 0;
    stroke-dasharray: 0 0 10 40 10 40;
    transition: 0.5s !important;
  }
`;

export default AnimatedOutlineNavbar;
