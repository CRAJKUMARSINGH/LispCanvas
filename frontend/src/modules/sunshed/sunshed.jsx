import React, { useState } from 'react';

const SunshedModule = () => {
  const [params, setParams] = useState({});

  return (
    <div style={{ padding: '20px' }}>
      <h2>Sunshed Design Module</h2>
      <p>Interactive canvas-based design tool for .</p>
      
      <div style={{ marginTop: '20px', display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <h3>Parameters</h3>
          <div style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px' }}>
            <p>Parameter inputs will go here</p>
          </div>
        </div>
        
        <div style={{ flex: 2 }}>
          <h3>Drawing Canvas</h3>
          <canvas 
            width="800" 
            height="600" 
            style={{ 
              border: '2px solid #ddd', 
              borderRadius: '4px',
              background: 'white'
            }}
          />
          <div style={{ marginTop: '10px' }}>
            <button style={{ marginRight: '10px', padding: '8px 16px' }}>Generate DXF</button>
            <button style={{ marginRight: '10px', padding: '8px 16px' }}>Export PDF</button>
            <button style={{ padding: '8px 16px' }}>Clear</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SunshedModule;
