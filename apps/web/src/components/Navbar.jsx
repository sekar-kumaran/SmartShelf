import React from 'react';
import { Eye, Layers, BarChart2, BookOpen, Clock, ShieldCheck, Sparkles, Store } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, healthInfo, onOpenModelCard }) {
  const tabs = [
    { id: 'inspector', label: 'Vision Inspector', icon: Eye },
    { id: 'analytics', label: 'Shelf Intelligence', icon: BarChart2 },
    { id: 'catalog', label: 'SKU Catalog (1,816)', icon: BookOpen },
    { id: 'history', label: 'Audit Log', icon: Clock },
  ];

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(7, 9, 14, 0.85)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '0.75rem 1.5rem',
    }}>
      <div style={{
        maxWidth: '1600px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        {/* Brand identity */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #3b82f6 0%, #10b981 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 15px rgba(59, 130, 246, 0.35)',
          }}>
            <Store size={22} color="#fff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontWeight: 800, fontSize: '1.25rem', letterSpacing: '-0.02em' }}>
                VIF <span style={{ color: '#3b82f6' }}>SmartShelf</span>
              </span>
              <span className="badge badge-blue">v0.1.0</span>
            </div>
            <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
              Indian Kirana & Retail Vision Intelligence
            </p>
          </div>
        </div>

        {/* Navigation tabs */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          background: 'rgba(255, 255, 255, 0.03)',
          padding: '4px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
        }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '7px 14px',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.825rem',
                  fontWeight: isActive ? 600 : 500,
                  color: isActive ? '#fff' : 'var(--text-muted)',
                  background: isActive ? 'linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.15) 100%)' : 'transparent',
                  border: isActive ? '1px solid rgba(59, 130, 246, 0.4)' : '1px solid transparent',
                  cursor: 'pointer',
                  transition: 'var(--transition)',
                }}
              >
                <Icon size={16} color={isActive ? '#60a5fa' : 'currentColor'} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Status / Model Card Action */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '5px 12px',
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.75rem',
            color: 'var(--text-muted)'
          }}>
            <div className={`pulse-dot ${healthInfo?.status === 'ready' ? 'online' : ''}`} />
            <span>{healthInfo?.status === 'ready' ? 'API Engine Active' : 'Connecting...'}</span>
          </div>

          <button
            onClick={onOpenModelCard}
            className="btn btn-secondary"
            style={{ fontSize: '0.75rem', padding: '6px 12px' }}
          >
            <ShieldCheck size={14} color="#10b981" />
            <span>Dataset & Model Card</span>
          </button>
        </div>
      </div>
    </header>
  );
}
