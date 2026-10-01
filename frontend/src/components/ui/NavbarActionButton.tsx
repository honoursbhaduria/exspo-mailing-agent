import React from 'react';
import styled from 'styled-components';

interface NavbarActionButtonProps {
  onClick?: () => void;
  title?: string;
}

export const NavbarActionButton: React.FC<NavbarActionButtonProps> = ({
  onClick,
  title = 'EDXSO System Status',
}) => {
  return (
    <StyledWrapper onClick={onClick}>
      <div className="icon-conatiner" title={title}>
        <svg width="19px" height="21px" viewBox="0 0 19 21" version="1.1" xmlns="http://www.w3.org/2000/svg">
          <g stroke="none" strokeWidth={1} fill="none" fillRule="evenodd">
            <g transform="translate(-142.000000, -122.000000)">
              <g transform="translate(142.000000, 122.000000)">
                <path d="M3.4,4 L11.5,4 L16,8.25 L16,17.6 C16,19.4777681 14.4777681,21 12.6,21 L3.4,21 C1.52223185,21 0,19.4777681 0,17.6 L0,7.4 C0,5.52223185 1.52223185,4 3.4,4 Z" fill="#BAE6FD" />
                <path d="M6.4,0 L12,0 L19,6.5 L19,14.6 C19,16.4777681 17.4777681,18 15.6,18 L6.4,18 C4.52223185,18 3,16.4777681 3,14.6 L3,3.4 C3,1.52223185 4.52223185,0 6.4,0 Z" fill="#7DD3FC" />
                <path d="M12,0 L12,5.5 C12,6.05228475 12.4477153,6.5 13,6.5 L19,6.5 L12,0 Z" fill="#38BDF8" />
              </g>
            </g>
          </g>
        </svg>
        <svg width="19px" height="21px" viewBox="0 0 19 21" version="1.1" xmlns="http://www.w3.org/2000/svg">
          <g stroke="none" strokeWidth={1} fill="none" fillRule="evenodd">
            <g transform="translate(-142.000000, -122.000000)">
              <g transform="translate(142.000000, 122.000000)">
                <path d="M3.4,4 L11.5,4 L16,8.25 L16,17.6 C16,19.4777681 14.4777681,21 12.6,21 L3.4,21 C1.52223185,21 0,19.4777681 0,17.6 L0,7.4 C0,5.52223185 1.52223185,4 3.4,4 Z" fill="#BAE6FD" />
                <path d="M6.4,0 L12,0 L19,6.5 L19,14.6 C19,16.4777681 17.4777681,18 15.6,18 L6.4,18 C4.52223185,18 3,16.4777681 3,14.6 L3,3.4 C3,1.52223185 4.52223185,0 6.4,0 Z" fill="#7DD3FC" />
                <path d="M12,0 L12,5.5 C12,6.05228475 12.4477153,6.5 13,6.5 L19,6.5 L12,0 Z" fill="#38BDF8" />
              </g>
            </g>
          </g>
        </svg>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  .icon-conatiner {
    width: 34px;
    height: 34px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    border-radius: 9px;
    border: 1px solid #BAE6FD;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    cursor: pointer;
    position: relative;
    transition: transform 0.15s ease;
  }

  .icon-conatiner svg {
    width: 17px;
    height: auto;
  }

  .icon-conatiner svg:last-child {
    position: absolute;
  }

  .icon-conatiner:active {
    animation: press 0.2s 1 linear;
  }

  .icon-conatiner:active svg:last-child {
    animation: bounce 0.2s 1 linear;
  }

  @keyframes press {
    0% { transform: scale(1); }
    50% { transform: scale(0.92); }
    to { transform: scale(1); }
  }

  @keyframes bounce {
    50% { transform: rotate(5deg) translate(4px, -8px); }
    to { transform: scale(0.9) rotate(10deg) translate(8px, -15px); opacity: 0; }
  }
`;

export default NavbarActionButton;
