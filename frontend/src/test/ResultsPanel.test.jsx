import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ResultsPanel from '../components/ResultsPanel'

describe('ResultsPanel', () => {
  it('renders no issues message when diagnostics are empty', () => {
    render(
      <ResultsPanel 
        diagnostics={[]} 
        onApplyFix={() => {}} 
        onJumpToLine={() => {}} 
      />
    )
    
    expect(screen.getByText(/No issues found/i)).toBeInTheDocument()
  })

  it('renders error diagnostics with red badge', () => {
    const diagnostics = [
      {
        severity: 'error',
        message: 'Test error message',
        line: 5,
        column: 10,
        ruleId: 'test-rule'
      }
    ]
    
    render(
      <ResultsPanel 
        diagnostics={diagnostics} 
        onApplyFix={() => {}} 
        onJumpToLine={() => {}} 
      />
    )
    
    expect(screen.getByText('Test error message')).toBeInTheDocument()
    expect(screen.getByText('Error')).toBeInTheDocument()
  })

  it('renders suggestion diagnostics with green badge', () => {
    const diagnostics = [
      {
        severity: 'suggestion',
        message: 'Test suggestion',
        line: 3,
        column: 1,
        ruleId: 'suggestion-rule'
      }
    ]
    
    render(
      <ResultsPanel 
        diagnostics={diagnostics} 
        onApplyFix={() => {}} 
        onJumpToLine={() => {}} 
      />
    )
    
    expect(screen.getByText('Test suggestion')).toBeInTheDocument()
    expect(screen.getByText('Suggestion')).toBeInTheDocument()
  })
})
