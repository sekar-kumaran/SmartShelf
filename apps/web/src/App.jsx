import React, { useEffect, useState, useCallback } from 'react';
import Navbar from './components/Navbar.jsx';
import UploadPanel from './components/UploadPanel.jsx';
import ShelfViewer from './components/ShelfViewer.jsx';
import AnalyticsPanel from './components/AnalyticsPanel.jsx';
import CatalogPanel from './components/CatalogPanel.jsx';
import AuditHistory from './components/AuditHistory.jsx';
import ModelCardModal from './components/ModelCardModal.jsx';

export default function App() {
  const [activeTab, setActiveTab] = useState('inspector');
  const [result, setResult] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [healthInfo, setHealthInfo] = useState(null);
  const [showModelCard, setShowModelCard] = useState(false);

  // Poll health endpoint
  useEffect(() => {
    const check = async () => {
      try {
        const res = await fetch('/health/ready');
        if (res.ok) setHealthInfo(await res.json());
      } catch { /* API not up yet */ }
    };
    check();
    const id = setInterval(check, 30000);
    return () => clearInterval(id);
  }, []);

  const handleResult = useCallback((data, url) => {
    setResult(data || null);
    setImageUrl(url || null);
    // Auto-switch to analytics when result arrives
    if (data) setActiveTab('analytics');
  }, []);

  return (
    <div style={{ minHeight: '100vh', position: 'relative', zIndex: 1 }}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        healthInfo={healthInfo}
        onOpenModelCard={() => setShowModelCard(true)}
      />

      <main style={{ maxWidth: '1600px', margin: '0 auto', padding: '1.5rem' }}>
        {activeTab === 'inspector' && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: '360px 1fr',
            gap: '1.5rem',
            alignItems: 'start',
          }}>
            {/* Left: Upload + controls */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ marginBottom: '1rem' }}>
                  <h1 style={{ fontWeight: 800, fontSize: '1.15rem', marginBottom: '4px' }}>
                    Vision Inspector
                  </h1>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    Upload a shelf photo to detect and count all grocery products
                  </p>
                </div>
                <UploadPanel
                  onResult={handleResult}
                  onLoading={setIsLoading}
                  isLoading={isLoading}
                />
              </div>

              {/* Quick stats when result is available */}
              {result && (
                <div className="glass-panel" style={{ padding: '1.25rem' }}>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '12px' }}>
                    Quick Summary
                  </p>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <SummaryRow label="Products Found" value={result.total_items_detected} color="#3b82f6" />
                    <SummaryRow label="Unique SKUs" value={result.unique_skus_detected} color="#10b981" />
                    <SummaryRow label="Shelf Occupancy" value={`${result.estimated_shelf_occupancy_pct.toFixed(1)}%`} color="#a78bfa" />
                    <SummaryRow label="Compliance" value={`${result.planogram_compliance_score.toFixed(0)}/100`} color="#fbbf24" />
                    {result.out_of_stock_gaps?.length > 0 && (
                      <SummaryRow label="OOS Alerts" value={result.out_of_stock_gaps.length} color="#f43f5e" />
                    )}
                  </div>
                  <button
                    className="btn btn-secondary"
                    style={{ width: '100%', marginTop: '14px', fontSize: '0.8rem' }}
                    onClick={() => setActiveTab('analytics')}
                  >
                    View Full Analytics →
                  </button>
                </div>
              )}
            </div>

            {/* Right: Shelf viewer */}
            <div className="glass-panel" style={{ padding: '1.5rem' }}>
              {result && imageUrl ? (
                <ShelfViewer imageUrl={imageUrl} result={result} />
              ) : (
                <EmptyViewerPlaceholder />
              )}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <AnalyticsPanel result={result} />
          </div>
        )}

        {activeTab === 'catalog' && (
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <CatalogPanel />
          </div>
        )}

        {activeTab === 'history' && (
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <AuditHistory />
          </div>
        )}
      </main>

      {showModelCard && <ModelCardModal onClose={() => setShowModelCard(false)} />}
    </div>
  );
}

function SummaryRow({ label, value, color }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{label}</span>
      <span style={{ fontSize: '0.9rem', fontWeight: 700, color }}>{value}</span>
    </div>
  );
}

function EmptyViewerPlaceholder() {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      gap: '1.5rem', minHeight: '420px',
      color: 'var(--text-dim)', textAlign: 'center',
    }}>
      <div style={{
        width: '80px', height: '80px',
        borderRadius: '24px',
        background: 'rgba(59, 130, 246, 0.07)',
        border: '1px solid rgba(59, 130, 246, 0.15)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="1.5">
          <rect x="2" y="3" width="20" height="18" rx="2" />
          <path d="M2 9h20M2 15h20M9 9v9M15 9v9" />
        </svg>
      </div>
      <div>
        <p style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
          No Shelf Analysed Yet
        </p>
        <p style={{ fontSize: '0.82rem', maxWidth: '360px' }}>
          Upload a photo of any Indian kirana shelf, supermarket gondola, or FMCG display to run product recognition and inventory intelligence.
        </p>
      </div>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', justifyContent: 'center' }}>
        {['Amul', 'Haldirams', 'Maggi', 'Britannia', 'Parle'].map((b) => (
          <span key={b} className="badge badge-blue">{b}</span>
        ))}
        <span className="badge badge-blue">+ 1,811 more SKUs</span>
      </div>
    </div>
  );
}
