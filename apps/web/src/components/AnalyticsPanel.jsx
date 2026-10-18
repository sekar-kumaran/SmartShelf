import React from 'react';
import { BarChart2, Package, Layers, AlertTriangle, ShieldCheck, TrendingUp, Clock } from 'lucide-react';

function MetricCard({ icon: Icon, label, value, unit = '', color = '#3b82f6', glow = 'rgba(59,130,246,0.25)' }) {
  return (
    <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '2px' }}>
        <div style={{
          width: '32px', height: '32px', borderRadius: '10px',
          background: `${color}1a`, display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <Icon size={16} color={color} />
        </div>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>{label}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
        <span style={{ fontSize: '1.85rem', fontWeight: 800, color, letterSpacing: '-0.03em' }}>{value}</span>
        {unit && <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{unit}</span>}
      </div>
    </div>
  );
}

function BrandBar({ brand, percentage, count, maxCount }) {
  const width = (count / maxCount) * 100;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>{brand}</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{count} items</span>
          <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', fontWeight: 600, color: '#60a5fa' }}>{percentage}%</span>
        </div>
      </div>
      <div style={{ height: '5px', background: 'rgba(255,255,255,0.06)', borderRadius: '9999px', overflow: 'hidden' }}>
        <div style={{
          width: `${width}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #3b82f6, #10b981)',
          borderRadius: '9999px',
          transition: 'width 0.8s cubic-bezier(0.16, 1, 0.3, 1)',
        }} />
      </div>
    </div>
  );
}

function GapCard({ gap }) {
  const isCritical = gap.severity === 'critical';
  return (
    <div style={{
      padding: '12px 14px',
      borderRadius: 'var(--radius-md)',
      background: isCritical ? 'rgba(244, 63, 94, 0.08)' : 'rgba(245, 158, 11, 0.08)',
      border: `1px solid ${isCritical ? 'rgba(244, 63, 94, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`,
      display: 'flex',
      alignItems: 'flex-start',
      gap: '10px',
    }}>
      <AlertTriangle size={16} color={isCritical ? '#f43f5e' : '#f59e0b'} style={{ flexShrink: 0, marginTop: '1px' }} />
      <div>
        <p style={{ fontSize: '0.8rem', fontWeight: 600, color: isCritical ? '#fb7185' : '#fbbf24', marginBottom: '3px' }}>
          {isCritical ? 'Critical Out-of-Stock' : 'Empty Shelf Slot'} — Row {gap.shelf_row}
        </p>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{gap.message}</p>
        <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', marginTop: '3px' }}>
          Gap zone: ({gap.bbox.x1.toFixed(0)}, {gap.bbox.y1.toFixed(0)}) → ({gap.bbox.x2.toFixed(0)}, {gap.bbox.y2.toFixed(0)}) px
        </p>
      </div>
    </div>
  );
}

function TierCard({ tier }) {
  return (
    <div className="glass-panel" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '6px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>Shelf Row {tier.row}</span>
        <span className={`badge ${tier.occupancy_percentage >= 85 ? 'badge-green' : tier.occupancy_percentage >= 60 ? 'badge-amber' : 'badge-rose'}`}>
          {tier.occupancy_percentage.toFixed(0)}% full
        </span>
      </div>
      <div style={{ display: 'flex', gap: '12px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        <span><strong style={{ color: 'var(--text-main)' }}>{tier.item_count}</strong> items</span>
        <span><strong style={{ color: 'var(--text-main)' }}>{tier.sku_count}</strong> unique SKUs</span>
        {tier.dominant_brand && (
          <span>Lead: <strong style={{ color: '#60a5fa' }}>{tier.dominant_brand}</strong></span>
        )}
      </div>
    </div>
  );
}

export default function AnalyticsPanel({ result }) {
  if (!result) {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        gap: '1rem', padding: '3rem', color: 'var(--text-dim)', textAlign: 'center',
      }}>
        <BarChart2 size={48} color="rgba(255,255,255,0.1)" />
        <p style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-muted)' }}>
          No shelf analysis yet
        </p>
        <p style={{ fontSize: '0.82rem' }}>Upload a shelf photo to see real-time inventory intelligence.</p>
      </div>
    );
  }

  const maxCount = Math.max(1, ...result.brand_breakdown.map((b) => b.count));

  const complianceColor =
    result.planogram_compliance_score >= 80 ? '#10b981' :
    result.planogram_compliance_score >= 55 ? '#f59e0b' : '#f43f5e';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Metrics grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: '1rem' }}>
        <MetricCard icon={Package} label="Items Detected" value={result.total_items_detected} color="#3b82f6" />
        <MetricCard icon={Layers} label="Unique SKUs" value={result.unique_skus_detected} color="#10b981" glow="rgba(16,185,129,0.25)" />
        <MetricCard icon={TrendingUp} label="Shelf Occupancy" value={result.estimated_shelf_occupancy_pct.toFixed(1)} unit="%" color="#a78bfa" />
        <MetricCard icon={ShieldCheck} label="Compliance Score" value={result.planogram_compliance_score.toFixed(0)} unit="/100" color={complianceColor} />
        <MetricCard icon={AlertTriangle} label="OOS Gaps" value={result.out_of_stock_gaps?.length || 0} color="#f43f5e" glow="rgba(244,63,94,0.25)" />
        <MetricCard icon={Clock} label="Inference Time" value={result.inference_time_ms?.toFixed(0)} unit="ms" color="#fbbf24" />
      </div>

      {/* Shelf Tier Map */}
      {result.shelf_tiers?.length > 0 && (
        <div>
          <p style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
            Shelf Tier Map
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {result.shelf_tiers.map((tier) => <TierCard key={tier.row} tier={tier} />)}
          </div>
        </div>
      )}

      {/* Brand breakdown */}
      {result.brand_breakdown?.length > 0 && (
        <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <p style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Brand Facing Distribution
          </p>
          {result.brand_breakdown.map((b) => (
            <BrandBar key={b.brand} brand={b.brand} percentage={b.percentage} count={b.count} maxCount={maxCount} />
          ))}
        </div>
      )}

      {/* OOS Alerts */}
      {result.out_of_stock_gaps?.length > 0 && (
        <div>
          <p style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
            Out-of-Stock Alerts
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {result.out_of_stock_gaps.map((gap, i) => <GapCard key={i} gap={gap} />)}
          </div>
        </div>
      )}

      {/* Audit metadata */}
      <div style={{
        padding: '10px 14px',
        borderRadius: 'var(--radius-md)',
        background: 'rgba(255,255,255,0.025)',
        border: '1px solid var(--border-subtle)',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '1.5rem',
        fontSize: '0.72rem',
        color: 'var(--text-dim)',
        fontFamily: 'var(--font-mono)',
      }}>
        <span>Audit ID: <strong style={{ color: 'var(--text-muted)' }}>{result.audit_id}</strong></span>
        <span>Model: <strong style={{ color: 'var(--text-muted)' }}>{result.model_version}</strong></span>
        <span>Size: <strong style={{ color: 'var(--text-muted)' }}>{result.image_width}×{result.image_height}</strong></span>
        <span>Timestamp: <strong style={{ color: 'var(--text-muted)' }}>{new Date(result.timestamp).toLocaleTimeString()}</strong></span>
      </div>
    </div>
  );
}
