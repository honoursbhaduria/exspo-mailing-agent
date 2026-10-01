import React from 'react';
import styled from 'styled-components';

export interface TabItem {
  id: string;
  label: string;
}

interface AnimatedOutlineNavbarProps {
  items: TabItem[];
  activeId: string;
  onSelect: (id: string) => void;
}

export const AnimatedOutlineNavbar: React.FC<AnimatedOutlineNavbarProps> = ({
  items,
  activeId,
  onSelect,
}) => {
  return (
    <NavWrapper>
      <div className="tab-list">
        {items.map((item) => {
          const isActive = item.id === activeId;
          return (
            <button
              key={item.id}
              className={`tab-btn ${isActive ? 'active' : ''}`}
              onClick={() => onSelect(item.id)}
            >
              <span>{item.label}</span>
              {isActive && <div className="active-line" />}
            </button>
          );
        })}
      </div>
    </NavWrapper>
  );
};

const NavWrapper = styled.div`
  width: 100%;
  margin-bottom: 24px;

  .tab-list {
    display: flex;
    align-items: center;
    gap: 32px;
    border-bottom: 2px solid #E2E8F0;
    padding: 0;
    background: transparent;
    overflow-x: auto;
  }

  .tab-btn {
    position: relative;
    background: transparent;
    border: none;
    padding: 12px 2px 14px 2px;
    cursor: pointer;
    outline: none;
    transition: all 0.2s ease;
    white-space: nowrap;

    span {
      font-family: 'Bricolage Grotesque', sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      color: #555555;
      transition: color 0.2s ease;
    }

    &:hover span {
      color: #000000;
    }

    &.active span {
      color: #000000;
      font-weight: 900;
    }

    .active-line {
      position: absolute;
      bottom: -2px;
      left: 0;
      right: 0;
      height: 3px;
      background-color: #000000;
      border-radius: 2px;
      animation: lineIn 0.2s ease-out;
    }
  }

  @keyframes lineIn {
    from {
      transform: scaleX(0.7);
      opacity: 0;
    }
    to {
      transform: scaleX(1);
      opacity: 1;
    }
  }
`;

export default AnimatedOutlineNavbar;
