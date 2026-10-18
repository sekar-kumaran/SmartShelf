import React, { useEffect, useState } from 'react';
import { Clock, Package, AlertTriangle, ShieldCheck, TrendingUp } from 'lucide-react';

export default function AuditHistory() {
  const [audits, setAudits] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('/api/v1/audits');
        const data = await res.json();
        setAudits(data);
      } catch {
        // Fallback demo data
        setAudits([]);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem' }}>
        <div style={{
          width: '32px', height: '32px', borderRadius: '50%',
          border: '3px solid rgba(59,130,246,0.2)', borderTopColor: '#3b82f6',
          animation: 'spin 0.8s linear infinite',
        }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h2 style={{ fontWeight: 800, fontSize: '1.1rem', marginBottom: '2px' }}>
            Shelf Audit History
          </h2>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Past kirana store and supermarket inventory scans
          </p>
        </div>
        <span className="badge badge-green">
          <Clock size={11} /> {audits.length} audit{audits.length !== 1 ? 's' : ''} logged
        </span>
      </div>

      {audits.length === 0 ? (
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center',
          gap: '1rem', padding: '3rem', color: 'var(--text-dim)', textAlign: 'center',
        }}>
          <Clock size={40} color="rgba(255,255,255,0.08)" />
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>No audits yet</p>
          <p style={{ fontSize: '0.8rem' }}>Perform a shelf scan to populate audit history.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {audits.map((audit, idx) => {
            const complianceColor =
              audit.compliance_score >= 80 ? '#10b981' :
              audit.compliance_score >= 55 ? '#f59e0b' : '#f43f5e';

            return (
              <div
                key={audit.audit_id || idx}
                className="glass-panel"
                style={{
                  padding: '1.25rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px',
                  position: 'relative',
                  overflow: 'hidden',
                }}
              >
                {/* Compliance glow stripe */}
                <div style={{
                  position: 'absolute', top: 0, left: 0, width: '3px', bottom: 0,
                  background: complianceColor,
                }} />

                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px', paddingLeft: '10px' }}>
                  <div>
                    <p style={{ fontWeight: 700, fontSize: '0.95rem' }}>
                      {audit.store_name || 'Unnamed Store'}
                    </p>
                    <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', marginTop: '3px' }}>
                      {audit.timestamp ? new Date(audit.timestamp).toLocaleString() : '—'}
                    </p>
                  </div>
                  <span className="badge badge-blue" style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem' }}>
                    {audit.audit_id?.slice(0, 22) || 'N/A'}
                  </span>
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))',
                  gap: '8px',
                  paddingLeft: '10px',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Package size={13} color="#3b82f6" />
                    <div>
                      <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Items</p>
                      <p style={{ fontSize: '0.9rem', fontWeight: 700 }}>{audit.items_detected}</p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <TrendingUp size={13} color="#a78bfa" />
                    <div>
                      <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Occupancy</p>
                      <p style={{ fontSize: '0.9rem', fontWeight: 700 }}>{audit.occupancy_pct?.toFixed(1)}%</p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <ShieldCheck size={13} color={complianceColor} />
                    <div>
                      <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Compliance</p>
                      <p style={{ fontSize: '0.9rem', fontWeight: 700, color: complianceColor }}>
                        {audit.compliance_score?.toFixed(0)}/100
                      </p>
                    </div>
                  </div>
                  {audit.void_gaps_count > 0 && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <AlertTriangle size={13} color="#f43f5e" />
                      <div>
                        <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>OOS Gaps</p>
                        <p style={{ fontSize: '0.9rem', fontWeight: 700, color: '#fb7185' }}>
                          {audit.void_gaps_count}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
