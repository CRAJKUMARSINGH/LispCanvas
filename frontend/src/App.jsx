import React, { useState } from 'react';
import BridgeModule from './modules/bridge/bridge';
import RectangleColumnModule from './modules/rectangle_column/rectangle_column';
import RoadLsectionModule from './modules/road_lsection/road_lsection';
import RoadPlanModule from './modules/road_plan/road_plan';
import RoadCrossSectionModule from './modules/road_cross_section/road_cross_section';
import PmgsyRoadModule from './modules/pmgsy_road/pmgsy_road';
import LintelModule from './modules/lintel/lintel';
import SunshedModule from './modules/sunshed/sunshed';
import TbeamLbeamModule from './modules/tbeam_lbeam/tbeam_lbeam';
import StaircaseModule from './modules/staircase/staircase';

const modules = [
  { id: 'bridge', name: 'Bridge Design', component: BridgeModule },
  { id: 'rectangle_column', name: 'Rectangle Column', component: RectangleColumnModule },
  { id: 'road_lsection', name: 'Road L-Section', component: RoadLsectionModule },
  { id: 'road_plan', name: 'Road Plan', component: RoadPlanModule },
  { id: 'road_cross_section', name: 'Road Cross Section', component: RoadCrossSectionModule },
  { id: 'pmgsy_road', name: 'PMGSY Road', component: PmgsyRoadModule },
  { id: 'lintel', name: 'Lintel', component: LintelModule },
  { id: 'sunshed', name: 'Sunshed', component: SunshedModule },
  { id: 'tbeam_lbeam', name: 'T-Beam/L-Beam', component: TbeamLbeamModule },
  { id: 'staircase', name: 'Staircase', component: StaircaseModule }
];

function App() {
  const [activeModule, setActiveModule] = useState('bridge');
  
  const ActiveComponent = modules.find(m => m.id === activeModule)?.component;

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      <nav style={{ width: '250px', borderRight: '1px solid #ccc', padding: '20px', background: '#f8f9fa' }}>
        <h1 style={{ fontSize: '24px', marginBottom: '20px', color: '#333' }}>LispCanvas</h1>
        <p style={{ fontSize: '12px', color: '#666', marginBottom: '20px' }}>Civil Engineering Design</p>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {modules.map(module => (
            <li key={module.id} style={{ marginBottom: '8px' }}>
              <button
                onClick={() => setActiveModule(module.id)}
                style={{
                  width: '100%',
                  padding: '12px',
                  textAlign: 'left',
                  background: activeModule === module.id ? '#007bff' : 'white',
                  color: activeModule === module.id ? 'white' : '#333',
                  border: '1px solid #ddd',
                  cursor: 'pointer',
                  borderRadius: '4px',
                  fontSize: '14px',
                  transition: 'all 0.2s'
                }}
              >
                {module.name}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <main style={{ flex: 1, padding: '20px', overflow: 'auto', background: 'white' }}>
        {ActiveComponent && <ActiveComponent />}
      </main>
    </div>
  );
}

export default App;
