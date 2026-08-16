import './App.css'
import { ServerConfigPanel } from './components/ServerConfigPanel/ServerConfigPanel'
import { ServerSettingsPanel } from './components/ServerSettingsPanel/ServerSettingsPanel'
import { ServerStatusPanel } from './components/ServerStatusPanel/ServerStatusPanel'
import { ServerRefreshButton } from './components/SeverRefreshButton/ServerRefreshButton'

function App() {
  return (
    <main className='App'>
      <h1 className='title'>AssignmentBridge</h1>

      <div className='panels'>
        <ServerStatusPanel />
        <ServerConfigPanel />
        <ServerSettingsPanel />
        <ServerRefreshButton />
      </div>
    </main>
  )
}

export default App
