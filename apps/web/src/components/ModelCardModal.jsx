import React from 'react';
import { X, Database, Shield, Cpu, Layers, BarChart2 } from 'lucide-react';

export default function ModelCardModal({ onClose }) {
  return (
    <div
      style={{
        position: 'fixed', inset: 0, zIndex: 200,
        background: 'rgba(7, 9, 14, 0.85)',
        backdropFilter: 'blur(8px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: '1rem',
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%', maxWidth: '720px', maxHeight: '90vh',
          overflowY: 'auto', padding: '2rem',
          display: 'flex', flexDirection: 'column', gap: '1.5rem',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '44px', height: '44px', borderRadius: '14px',
              background: 'linear-gradient(135deg, #3b82f6 0%, #10b981 100%)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 4px 15px rgba(59, 130, 246, 0.35)',
            }}>
              <Cpu size={22} color="#fff" />
            </div>
            <div>
              <h2 style={{ fontWeight: 800, fontSize: '1.2rem' }}>Model & Dataset Card</h2>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>VIF SmartShelf — v0.1.0</p>
            </div>
          </div>
          <button onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: '6px' }}>
            <X size={20} />
          </button>
        </div>

        {/* Dataset section */}
        <Section icon={Database} title="Dataset: Indian Grocery Items" badge="Public Domain">
          <Table rows={[
            ['Source', 'IIT Patna, Roboflow Universe'],
            ['License', 'Public Domain — unrestricted commercial use'],
            ['Total Images', '5,983 (Train: 4,922 / Valid: 750 / Test: 311)'],
            ['Total Annotations', '76,306 normalized retail bounding boxes'],
            ['Classes', '1,816 authentic Indian FMCG SKUs'],
            ['Top Brands', 'Amul, Maggi, Britannia, Haldirams, Parle, Cadbury, Catch, Vim, RedLabel, Chings'],
            ['Polygon Annotations', '14,176 converted to YOLO bbox via ml/src/convert_annotations.py'],
            ['Integrity', '0 corrupt images — 100% clean splits'],
          ]} />
        </Section>

        {/* Model section */}
        <Section icon={Cpu} title="Model Architecture" badge="YOLOv8m">
          <Table rows={[
            ['Base Architecture', 'YOLOv8m (Ultralytics) — anchor-free detection head'],
            ['Task', 'Multiclass Object Detection'],
            ['Input Resolution', '640 × 640 × 3 (RGB)'],
            ['Pretrained Backbone', 'COCO 2017 ImageNet pretraining'],
            ['Fine-tuning', 'Full fine-tune on 1,816-class Indian grocery data'],
            ['Export Formats', 'PyTorch (.pt) · ONNX (.onnx) · TensorRT (.engine)'],
          ]} />
        </Section>

        {/* Performance targets */}
        <Section icon={BarChart2} title="Performance Targets" badge="Benchmarks">
          <Table rows={[
            ['mAP@0.50', '≥ 0.72 on test split'],
            ['mAP@0.50:0.95', '≥ 0.54 on test split'],
            ['Facing Count Accuracy', '≥ 92% match vs manual count'],
            ['CPU Latency (640×640)', '< 120 ms single image'],
            ['GPU Latency (T4/RTX)', '< 18 ms single image'],
          ]} />
        </Section>

        {/* Augmentation */}
        <Section icon={Layers} title="Training Augmentation" badge="Config">
          <Table rows={[
            ['HSV Jitter (s=0.7, v=0.4)', 'Handles diverse Kirana store lighting conditions'],
            ['Mosaic (1.0)', 'Dense shelf context for multi-product images'],
            ['MixUp (0.15)', 'Occlusion robustness for overlapping packages'],
            ['Scale (0.5)', 'Detects products at varied distances from shelf'],
            ['FlipUD', 'Disabled — shelves are not upside-down'],
            ['Epochs', '50 with AdamW optimizer, LR=0.001, patience=10'],
          ]} />
        </Section>

        {/* License */}
        <Section icon={Shield} title="License & Attribution" badge="Required">
          <div style={{
            padding: '14px 16px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(16, 185, 129, 0.06)',
            border: '1px solid rgba(16, 185, 129, 0.2)',
            fontSize: '0.8rem',
            color: 'var(--text-muted)',
            lineHeight: 1.7,
          }}>
            <strong style={{ color: 'var(--text-main)' }}>Dataset License:</strong> Public Domain — IIT Patna / Roboflow Universe.<br />
            Commercial use, training, redistribution — all permitted without restriction.<br /><br />
            <strong style={{ color: 'var(--text-main)' }}>Ethical Use:</strong> This system is designed exclusively for inventory intelligence and planogram compliance in physical retail environments. Not intended for person identification, biometric analysis, or surveillance without informed consent.
          </div>
        </Section>

        <button className="btn btn-primary" style={{ alignSelf: 'flex-end' }} onClick={onClose}>
          Close Card
        </button>
      </div>
    </div>
  );
}

function Section({ icon: Icon, title, badge, children }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Icon size={16} color="#3b82f6" />
        <h3 style={{ fontWeight: 700, fontSize: '0.95rem' }}>{title}</h3>
        <span className="badge badge-blue" style={{ marginLeft: '4px' }}>{badge}</span>
      </div>
      {children}
    </div>
  );
}

function Table({ rows }) {
  return (
    <div style={{
      borderRadius: 'var(--radius-md)',
      border: '1px solid var(--border-subtle)',
      overflow: 'hidden',
    }}>
      {rows.map(([label, value], i) => (
        <div key={i} style={{
          display: 'flex',
          gap: '1rem',
          padding: '10px 14px',
          background: i % 2 === 0 ? 'rgba(255,255,255,0.015)' : 'transparent',
          borderBottom: i < rows.length - 1 ? '1px solid var(--border-subtle)' : 'none',
        }}>
          <span style={{ minWidth: '180px', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>
            {label}
          </span>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-main)' }}>{value}</span>
        </div>
      ))}
    </div>
  );
}
