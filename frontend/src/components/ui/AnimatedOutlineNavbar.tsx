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
      <div className="tab-list no-scrollbar">
        {items.map((item) => {
          const isActive = item.id === activeId;
          return (
            <button
              key={item.id}
              type="button"
              className={`tab-btn ${isActive ? 'active' : ''}`}
              onClick={(e) => {
                onSelect(item.id);
                e.currentTarget.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
              }}
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
  margin-bottom: 20px;
  position: relative;

  .tab-list {
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 2px solid #E2E8F0;
    padding: 0 4px;
    background: transparent;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
    scroll-padding: 16px;
    scrollbar-width: none;
    &::-webkit-scrollbar {
      display: none;
    }

    @media (min-width: 640px) {
      gap: 20px;
    }

    @media (min-width: 1024px) {
      gap: 28px;
    }
  }

  .tab-btn {
    position: relative;
    flex-shrink: 0;
    background: transparent;
    border: none;
    padding: 10px 4px 12px 4px;
    cursor: pointer;
    outline: none;
    transition: all 0.2s ease;
    white-space: nowrap;
    -webkit-tap-highlight-color: transparent;

    @media (min-width: 640px) {
      padding: 12px 6px 14px 6px;
    }

    span {
      font-family: 'Bricolage Grotesque', sans-serif;
      font-size: 0.85rem;
      font-weight: 700;
      color: #555555;
      transition: color 0.2s ease;

      @media (min-width: 640px) {
        font-size: 0.95rem;
      }
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
