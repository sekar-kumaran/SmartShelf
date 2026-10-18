import React, { useEffect, useState, useCallback } from 'react';
import { Search, Package, Tag } from 'lucide-react';

const CATEGORY_COLORS = {
  'Personal Care & Hygiene': '#a78bfa',
  'Biscuits & Bakery': '#fbbf24',
  'Snacks & Namkeen': '#f97316',
  'Beverages': '#38bdf8',
  'Instant Foods & Sauces': '#fb7185',
  'Staples & Spices': '#4ade80',
  'Confectionery': '#e879f9',
  'Packaged Foods': '#94a3b8',
};

function CategoryPill({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '5px 12px',
        borderRadius: '9999px',
        fontSize: '0.76rem',
        fontWeight: 600,
        border: `1px solid ${active ? CATEGORY_COLORS[label] || '#3b82f6' : 'var(--border-subtle)'}`,
        background: active ? `${CATEGORY_COLORS[label] || '#3b82f6'}20` : 'transparent',
        color: active ? (CATEGORY_COLORS[label] || '#3b82f6') : 'var(--text-muted)',
        cursor: 'pointer',
        transition: 'var(--transition)',
        whiteSpace: 'nowrap',
      }}
    >
      {label}
    </button>
  );
}

export default function CatalogPanel() {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [total, setTotal] = useState(0);
  const [query, setQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const LIMIT = 60;

  const fetchCatalog = useCallback(async (q, cat, off) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ limit: LIMIT, offset: off });
      if (q) params.append('q', q);
      if (cat) params.append('category', cat);
      const res = await fetch(`/api/v1/catalog?${params}`);
      if (!res.ok) throw new Error('API error');
      const data = await res.json();
      setItems(data.items);
      setTotal(data.total);
      if (!cat) setCategories(data.categories || []);
    } catch {
      // Keep existing data on error
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const tid = setTimeout(() => {
      setOffset(0);
      fetchCatalog(query, activeCategory, 0);
    }, 280);
    return () => clearTimeout(tid);
  }, [query, activeCategory, fetchCatalog]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontWeight: 800, fontSize: '1.1rem', marginBottom: '2px' }}>Indian Grocery SKU Catalog</h2>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            {total.toLocaleString()} products / 1,816 total classes — IIT Patna dataset (Public Domain)
          </p>
        </div>
        <div className="badge badge-blue">
          <Tag size={11} /> 1,816 SKUs
        </div>
      </div>

      {/* Search */}
      <div style={{ position: 'relative' }}>
        <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }} />
        <input
          type="text"
          placeholder="Search: Amul, Maggi, Haldirams, Parle, Britannia..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{
            width: '100%',
            padding: '10px 12px 10px 40px',
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--text-main)',
            fontSize: '0.875rem',
            fontFamily: 'var(--font-sans)',
            outline: 'none',
            transition: 'var(--transition)',
          }}
          onFocus={(e) => { e.target.style.borderColor = '#3b82f6'; }}
          onBlur={(e) => { e.target.style.borderColor = 'var(--border-subtle)'; }}
        />
      </div>

      {/* Category filter */}
      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
        <CategoryPill
          label="All Categories"
          active={activeCategory === null}
          onClick={() => setActiveCategory(null)}
        />
        {categories.map((cat) => (
          <CategoryPill
            key={cat}
            label={cat}
            active={activeCategory === cat}
            onClick={() => setActiveCategory(cat === activeCategory ? null : cat)}
          />
        ))}
      </div>

      {/* Grid */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem', color: 'var(--text-dim)' }}>
          <div className="spinner" style={{ width: '32px', height: '32px' }} />
          <style>{`.spinner { border: 3px solid rgba(59,130,246,0.2); border-top-color: #3b82f6; border-radius: 50%; animation: spin 0.8s linear infinite; } @keyframes spin { to { transform: rotate(360deg); } }`}</style>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
          gap: '10px',
        }}>
          {items.map((item) => {
            const color = CATEGORY_COLORS[item.category] || '#94a3b8';
            return (
              <div
                key={item.class_id}
                className="glass-panel"
                style={{
                  padding: '1rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px',
                  position: 'relative',
                  overflow: 'hidden',
                }}
              >
                {/* Color accent stripe */}
                <div style={{
                  position: 'absolute',
                  top: 0, left: 0, right: 0,
                  height: '3px',
                  background: color,
                  opacity: 0.7,
                }} />

                <div style={{
                  width: '36px', height: '36px',
                  borderRadius: '10px',
                  background: `${color}18`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  <Package size={18} color={color} />
                </div>
                <div>
                  <p style={{ fontSize: '0.82rem', fontWeight: 700, wordBreak: 'break-word', lineHeight: 1.3 }}>
                    {item.name}
                  </p>
                  <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '3px' }}>{item.category}</p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                    ID #{item.class_id}
                  </span>
                  {item.popular && (
                    <span className="badge badge-amber" style={{ fontSize: '0.6rem', padding: '2px 6px' }}>
                      Popular
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Pagination */}
      {total > LIMIT && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', paddingTop: '0.5rem' }}>
          <button className="btn btn-secondary" disabled={offset === 0}
            onClick={() => { const n = Math.max(0, offset - LIMIT); setOffset(n); fetchCatalog(query, activeCategory, n); }}>
            ← Previous
          </button>
          <span style={{ padding: '8px 14px', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
            {offset + 1}–{Math.min(offset + LIMIT, total)} of {total.toLocaleString()}
          </span>
          <button className="btn btn-secondary" disabled={offset + LIMIT >= total}
            onClick={() => { const n = offset + LIMIT; setOffset(n); fetchCatalog(query, activeCategory, n); }}>
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
