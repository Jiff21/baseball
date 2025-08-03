/**
 * Accordion component for collapsible content sections
 */
import React, { useState, useRef, useEffect } from 'react';
import './Accordion.css';

interface AccordionProps {
  title: string;
  children: React.ReactNode;
  isOpen: boolean;
  onToggle: () => void;
  className?: string;
}

const Accordion: React.FC<AccordionProps> = ({
  title,
  children,
  isOpen,
  onToggle,
  className = ''
}) => {
  const contentRef = useRef<HTMLDivElement>(null);
  const [contentHeight, setContentHeight] = useState<number>(0);

  useEffect(() => {
    if (contentRef.current) {
      setContentHeight(isOpen ? contentRef.current.scrollHeight : 0);
    }
  }, [isOpen, children]);

  return (
    <div className={`accordion ${className}`}>
      <button
        className={`accordion-header ${isOpen ? 'open' : ''}`}
        onClick={onToggle}
        type="button"
        aria-expanded={isOpen}
      >
        <h3 className="accordion-title">{title}</h3>
        <span className={`accordion-icon ${isOpen ? 'open' : ''}`}>
          ▼
        </span>
      </button>
      
      <div
        className={`accordion-content ${isOpen ? 'open' : ''}`}
        style={{ height: contentHeight }}
      >
        <div ref={contentRef} className="accordion-content-inner">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Accordion;

