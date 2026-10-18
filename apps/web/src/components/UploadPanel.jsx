import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Upload, Camera, Zap, Image as ImageIcon, X, AlertCircle, Sparkles } from 'lucide-react';

export default function UploadPanel({ onResult, onLoading, isLoading }) {
  const [dragOver, setDragOver] = useState(false);
  const [preview, setPreview] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);
  const [error, setError] = useState(null);
  const [confidence, setConfidence] = useState(0.08);
  const [iou, setIou] = useState(0.55);
  const [samples, setSamples] = useState([]);
  const fileRef = useRef();

  useEffect(() => {
    fetch('/api/v1/sample-shelves')
      .then((r) => r.json())
      .then((d) => setSamples(d.samples || []))
      .catch(() => {});
  }, []);

  const processFile = useCallback(async (file, confVal = null, iouVal = null) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (JPEG, PNG, WebP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image must be smaller than 10 MB.');
      return;
    }
    setError(null);
    setCurrentFile(file);
    const url = URL.createObjectURL(file);
    setPreview(url);

    const c = confVal !== null ? confVal : confidence;
    const i = iouVal !== null ? iouVal : iou;

    // Build multipart form
    const form = new FormData();
    form.append('file', file);
    form.append('confidence', c);
    form.append('iou', i);

    try {
      onLoading(true);
      const res = await fetch('/api/v1/predict', { method: 'POST', body: form });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || `Server error ${res.status}`);
      }
      const data = await res.json();
      onResult(data, url);
    } catch (e) {
      setError(e.message);
    } finally {
      onLoading(false);
    }
  }, [confidence, iou, onLoading, onResult]);

  const loadSample = useCallback(async (sample) => {
    try {
      onLoading(true);
      setError(null);
      const res = await fetch(`/static/samples/${sample.filename}`);
      if (!res.ok) throw new Error('Could not fetch sample image');
      const blob = await res.blob();
      const file = new File([blob], sample.filename, { type: 'image/jpeg' });
      processFile(file);
    } catch (err) {
      setError(`Failed to load sample: ${err.message}`);
      onLoading(false);
    }
  }, [processFile, onLoading]);

  const onDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    processFile(file);
  }, [processFile]);

  const onFileChange = useCallback((e) => {
    processFile(e.target.files[0]);
  }, [processFile]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Drop zone */}
      <div
        onClick={() => fileRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        style={{
          border: `2px dashed ${dragOver ? '#3b82f6' : 'var(--border-subtle)'}`,
          borderRadius: 'var(--radius-lg)',
          padding: '2.5rem 1.5rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '1rem',
          cursor: 'pointer',
          background: dragOver
            ? 'rgba(59, 130, 246, 0.07)'
            : preview
            ? 'transparent'
            : 'rgba(255, 255, 255, 0.018)',
          transition: 'var(--transition)',
          position: 'relative',
          overflow: 'hidden',
          minHeight: '220px',
        }}
      >
        {preview ? (
          <>
            <img
              src={preview}
              alt="Shelf preview"
              style={{
                width: '100%',
                maxHeight: '280px',
                objectFit: 'cover',
                borderRadius: 'var(--radius-md)',
                opacity: isLoading ? 0.45 : 1,
                transition: 'opacity 0.3s',
              }}
            />
            {isLoading && (
              <div style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                background: 'rgba(7, 9, 14, 0.6)',
                backdropFilter: 'blur(4px)',
              }}>
                <div className="spinner" />
                <p style={{ color: '#60a5fa', fontSize: '0.875rem', fontWeight: 600 }}>
                  Running YOLO inference...
                </p>
              </div>
            )}
            {!isLoading && (
              <button
                onClick={(e) => { e.stopPropagation(); setPreview(null); onResult(null); }}
                style={{
                  position: 'absolute',
                  top: '10px',
                  right: '10px',
                  background: 'rgba(0,0,0,0.6)',
                  border: 'none',
                  borderRadius: '50%',
                  width: '30px',
                  height: '30px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  color: '#fff',
                }}
              >
                <X size={16} />
              </button>
            )}
          </>
        ) : (
          <>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '20px',
              background: 'rgba(59, 130, 246, 0.1)',
              border: '1px solid rgba(59, 130, 246, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <Upload size={30} color="#3b82f6" />
            </div>
            <div style={{ textAlign: 'center' }}>
              <p style={{ fontWeight: 700, fontSize: '1rem', marginBottom: '4px' }}>
                Drop a shelf photo here
              </p>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                Supports JPEG · PNG · WebP up to 10 MB
              </p>
            </div>
            <span className="badge badge-blue">Click to browse</span>
          </>
        )}
        <input
          ref={fileRef}
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={onFileChange}
        />
      </div>

      {/* Quick Test Samples */}
      {samples.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Quick Test: Indian Kirana Samples
            </span>
            <span className="badge badge-purple" style={{ fontSize: '0.68rem', display: 'flex', alignItems: 'center', gap: '3px' }}>
              <Sparkles size={11} /> 1-Click Run
            </span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem' }}>
            {samples.slice(0, 3).map((s, idx) => (
              <button
                key={s.id}
                type="button"
                disabled={isLoading}
                onClick={() => loadSample(s)}
                style={{
                  padding: '9px 10px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-subtle)',
                  background: 'rgba(255, 255, 255, 0.03)',
                  color: 'var(--text-primary)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  cursor: isLoading ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  if (!isLoading) {
                    e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.6)';
                    e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)';
                  }
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--border-subtle)';
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)';
                }}
              >
                <Camera size={13} color="#3b82f6" />
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  Shelf #{idx + 1}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <p style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          Inference Controls
        </p>
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Confidence Threshold</label>
            <span className="badge badge-blue">{confidence.toFixed(2)}</span>
          </div>
          <input type="range" min={0.01} max={0.80} step={0.01} value={confidence}
            onChange={(e) => setConfidence(parseFloat(e.target.value))} />
        </div>
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>NMS IoU Threshold</label>
            <span className="badge badge-blue">{iou.toFixed(2)}</span>
          </div>
          <input type="range" min={0.1} max={0.9} step={0.01} value={iou}
            onChange={(e) => setIou(parseFloat(e.target.value))} />
        </div>

        {/* Tip for 1,816-class Model */}
        <div style={{
          padding: '8px 12px',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(59, 130, 246, 0.08)',
          border: '1px solid rgba(59, 130, 246, 0.2)',
          fontSize: '0.73rem',
          color: '#93c5fd',
          lineHeight: 1.4
        }}>
          💡 <strong>Tip for 1,816 SKU Model:</strong> Probability is divided across 1,816 products. Set confidence between <strong>0.05 – 0.12</strong> to detect all occluded and dense shelf jars.
        </div>

        {preview && currentFile && (
          <button
            type="button"
            className="btn btn-primary"
            style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', background: 'linear-gradient(135deg, #2563eb, #3b82f6)' }}
            disabled={isLoading}
            onClick={() => processFile(currentFile)}
          >
            <Zap size={15} />
            <span>Re-run at Conf {confidence.toFixed(2)}</span>
          </button>
        )}

        <button
          type="button"
          className="btn btn-secondary"
          style={{ width: '100%', marginTop: preview ? '2px' : '4px' }}
          disabled={isLoading}
          onClick={() => fileRef.current?.click()}
        >
          <ImageIcon size={16} />
          <span>{preview ? 'Select Different Image' : 'Select Shelf Image'}</span>
        </button>
      </div>

      {/* Error */}
      {error && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '12px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(244, 63, 94, 0.1)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          color: '#fb7185',
          fontSize: '0.82rem',
        }}>
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* Spinner style */}
      <style>{`
        .spinner {
          width: 40px; height: 40px;
          border: 3px solid rgba(59, 130, 246, 0.2);
          border-top-color: #3b82f6;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}
