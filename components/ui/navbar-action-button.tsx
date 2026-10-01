import React from 'react';
import styled from 'styled-components';

interface NavbarActionButtonProps {
  onClick?: () => void;
  title?: string;
}

export const NavbarActionButton: React.FC<NavbarActionButtonProps> = ({ onClick, title = 'Export Records' }) => {
  return (
    <StyledWrapper onClick={onClick}>
      <div className="icon-conatiner" title={title}>
        <svg width="19px" height="21px" viewBox="0 0 19 21" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
          <title>Group</title>
          <g id="Page-1" stroke="none" strokeWidth={1} fill="none" fillRule="evenodd">
            <g id="Artboard" transform="translate(-142.000000, -122.000000)">
              <g id="Group" transform="translate(142.000000, 122.000000)">
                <path d="M3.4,4 L11.5,4 L11.5,4 L16,8.25 L16,17.6 C16,19.4777681 14.4777681,21 12.6,21 L3.4,21 C1.52223185,21 6.74049485e-16,19.4777681 0,17.6 L0,7.4 C2.14128934e-16,5.52223185 1.52223185,4 3.4,4 Z" id="Rectangle-Copy" fill="#C4FFE4" />
                <path d="M6.4,0 L12,0 L12,0 L19,6.5 L19,14.6 C19,16.4777681 17.4777681,18 15.6,18 L6.4,18 C4.52223185,18 3,16.4777681 3,14.6 L3,3.4 C3,1.52223185 4.52223185,7.89029623e-16 6.4,0 Z" id="Rectangle" fill="#85EBBC" />
                <path d="M12,0 L12,5.5 C12,6.05228475 12.4477153,6.5 13,6.5 L19,6.5 L19,6.5 L12,0 Z" id="Path-2" fill="#64B18D" />
              </g>
            </g>
          </g>
        </svg>
        <svg width="19px" height="21px" viewBox="0 0 19 21" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
          <title>Group</title>
          <g id="Page-1" stroke="none" strokeWidth={1} fill="none" fillRule="evenodd">
            <g id="Artboard" transform="translate(-142.000000, -122.000000)">
              <g id="Group" transform="translate(142.000000, 122.000000)">
                <path d="M3.4,4 L11.5,4 L11.5,4 L16,8.25 L16,17.6 C16,19.4777681 14.4777681,21 12.6,21 L3.4,21 C1.52223185,21 6.74049485e-16,19.4777681 0,17.6 L0,7.4 C2.14128934e-16,5.52223185 1.52223185,4 3.4,4 Z" id="Rectangle-Copy" fill="#C4FFE4" />
                <path d="M6.4,0 L12,0 L12,0 L19,6.5 L19,14.6 C19,16.4777681 17.4777681,18 15.6,18 L6.4,18 C4.52223185,18 3,16.4777681 3,14.6 L3,3.4 C3,1.52223185 4.52223185,7.89029623e-16 6.4,0 Z" id="Rectangle" fill="#85EBBC" />
                <path d="M12,0 L12,5.5 C12,6.05228475 12.4477153,6.5 13,6.5 L19,6.5 L19,6.5 L12,0 Z" id="Path-2" fill="#64B18D" />
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
    width: 52px;
    height: 52px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #fff;
    border-radius: 14px;
    border: 1px solid #ECEFF8;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    cursor: pointer;
    position: relative;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }

  .icon-conatiner:hover {
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  }

  .icon-conatiner svg {
    width: 22px;
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
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(0.92);
    }
    to {
      transform: scale(1);
    }
  }

  @keyframes bounce {
    50% {
      transform: rotate(5deg) translate(8px, -15px);
    }
    to {
      transform: scale(0.9) rotate(10deg) translate(18px, -28px);
      opacity: 0;
    }
  }
`;

export default NavbarActionButton;
