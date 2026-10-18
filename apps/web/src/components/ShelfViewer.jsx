import React, { useEffect, useRef, useState } from 'react';
import { Tag, Package, AlertTriangle } from 'lucide-react';

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

function getColor(category) {
  return CATEGORY_COLORS[category] || '#94a3b8';
}

export default function ShelfViewer({ imageUrl, result }) {
  const canvasRef = useRef(null);
  const imgRef = useRef(null);
  const [hoveredId, setHoveredId] = useState(null);
  const [rendered, setRendered] = useState(false);

  useEffect(() => {
    if (!imageUrl || !result) { setRendered(false); return; }
    const img = imgRef.current;
    const canvas = canvasRef.current;
    if (!img || !canvas) return;

    const draw = () => {
      const ctx = canvas.getContext('2d');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);

      const scaleX = img.naturalWidth / result.image_width;
      const scaleY = img.naturalHeight / result.image_height;

      // Draw void gaps (red translucent)
      result.out_of_stock_gaps?.forEach((gap) => {
        const { x1, y1, width, height } = gap.bbox;
        ctx.save();
        ctx.fillStyle = 'rgba(244, 63, 94, 0.2)';
        ctx.strokeStyle = '#f43f5e';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
        ctx.fillRect(x1 * scaleX, y1 * scaleY, width * scaleX, height * scaleY);
        ctx.strokeRect(x1 * scaleX, y1 * scaleY, width * scaleX, height * scaleY);
        // Label
        ctx.fillStyle = '#f43f5e';
        ctx.font = `bold ${Math.max(11, Math.round(canvas.width / 80))}px Plus Jakarta Sans, sans-serif`;
        ctx.fillText('⚠ OOS Gap', x1 * scaleX + 4, y1 * scaleY + 16);
        ctx.restore();
      });

      // Draw detections
      result.detections?.forEach((det) => {
        const color = getColor(det.category);
        const isHovered = det.id === hoveredId;
        const { x1, y1, width, height } = det.bbox;

        ctx.save();
        ctx.strokeStyle = color;
        ctx.lineWidth = isHovered ? 3 : 2;
        ctx.fillStyle = isHovered ? `${color}22` : `${color}11`;
        ctx.fillRect(x1 * scaleX, y1 * scaleY, width * scaleX, height * scaleY);
        ctx.strokeRect(x1 * scaleX, y1 * scaleY, width * scaleX, height * scaleY);

        // Label box
        const fontSize = Math.max(10, Math.round(canvas.width / 90));
        ctx.font = `600 ${fontSize}px Plus Jakarta Sans, sans-serif`;
        const label = `${det.class_name.slice(0, 14)} ${(det.confidence * 100).toFixed(0)}%`;
        const textW = ctx.measureText(label).width + 8;
        ctx.fillStyle = color;
        ctx.fillRect(x1 * scaleX, (y1 * scaleY) - fontSize - 6, textW, fontSize + 6);
        ctx.fillStyle = '#07090e';
        ctx.fillText(label, x1 * scaleX + 4, (y1 * scaleY) - 3);
        ctx.restore();
      });

      setRendered(true);
    };

    if (img.complete) draw();
    else img.onload = draw;
  }, [imageUrl, result, hoveredId]);

  if (!imageUrl || !result) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {/* Canvas shelf view */}
      <div style={{ position: 'relative', borderRadius: 'var(--radius-lg)', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
        <img ref={imgRef} src={imageUrl} alt="shelf" style={{ display: 'none' }} />
        <canvas
          ref={canvasRef}
          style={{
            width: '100%',
            height: 'auto',
            display: 'block',
            borderRadius: 'var(--radius-lg)',
          }}
        />
        {/* Stats overlay */}
        <div style={{
          position: 'absolute',
          bottom: '12px',
          left: '12px',
          display: 'flex',
          gap: '8px',
          flexWrap: 'wrap',
        }}>
          <div className="badge badge-green" style={{ backdropFilter: 'blur(8px)', background: 'rgba(16, 185, 129, 0.7)' }}>
            <Package size={12} /> {result.total_items_detected} items
          </div>
          <div className="badge badge-blue" style={{ backdropFilter: 'blur(8px)', background: 'rgba(59, 130, 246, 0.7)' }}>
            <Tag size={12} /> {result.unique_skus_detected} unique SKUs
          </div>
          {result.out_of_stock_gaps?.length > 0 && (
            <div className="badge badge-rose" style={{ backdropFilter: 'blur(8px)', background: 'rgba(244, 63, 94, 0.7)' }}>
              <AlertTriangle size={12} /> {result.out_of_stock_gaps.length} OOS gap{result.out_of_stock_gaps.length !== 1 ? 's' : ''}
            </div>
          )}
        </div>
        {/* Inference time */}
        <div style={{
          position: 'absolute',
          top: '12px',
          right: '12px',
          background: 'rgba(7, 9, 14, 0.8)',
          backdropFilter: 'blur(8px)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-full)',
          padding: '4px 10px',
          fontSize: '0.7rem',
          fontFamily: 'var(--font-mono)',
          color: '#60a5fa',
        }}>
          {result.inference_time_ms?.toFixed(0)} ms
        </div>
      </div>

      {/* Detection list */}
      <div className="glass-panel" style={{ padding: '1rem', maxHeight: '260px', overflowY: 'auto' }}>
        <p style={{ fontSize: '0.76rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
          Detection List ({result.detections?.length || 0})
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          {result.detections?.map((det) => (
            <div
              key={det.id}
              onMouseEnter={() => setHoveredId(det.id)}
              onMouseLeave={() => setHoveredId(null)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '7px 10px',
                borderRadius: 'var(--radius-sm)',
                background: hoveredId === det.id ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                border: `1px solid ${hoveredId === det.id ? 'rgba(59, 130, 246, 0.3)' : 'transparent'}`,
                cursor: 'default',
                transition: 'var(--transition)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div style={{
                  width: '8px', height: '8px', borderRadius: '50%',
                  background: getColor(det.category), flexShrink: 0,
                }} />
                <div>
                  <p style={{ fontSize: '0.8rem', fontWeight: 600 }}>{det.class_name}</p>
                  <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>{det.category}</p>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {det.shelf_row && (
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                    Row {det.shelf_row}
                  </span>
                )}
                <span style={{
                  fontSize: '0.7rem',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 600,
                  color: det.confidence > 0.8 ? '#10b981' : det.confidence > 0.6 ? '#fbbf24' : '#f43f5e',
                }}>
                  {(det.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
