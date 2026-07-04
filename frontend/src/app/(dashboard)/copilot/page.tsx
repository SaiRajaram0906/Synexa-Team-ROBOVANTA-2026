'use client';

import { useState, useRef, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

export default function CopilotPage() {
  const [messages, setMessages] = useState<any[]>([
    {
      role: 'assistant',
      content: 'Hello! I am your AI Executive Orchestrator. I coordinate the Marketing, Sales, Operations, and Finance agents to synthesize business strategies. Ask me anything about your current campaigns, growth strategies, or KPIs.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedBizId, setSelectedBizId] = useState('00000000-0000-0000-0000-000000000000');
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const response = await apiClient.get('/business/');
        if (response.length > 0) {
          // Talk about the latest selected/created business context
          setSelectedBizId(response[response.length - 1].id);
        }
      } catch (err) {
        console.error(err);
      }
    }
    loadBusinesses();
  }, []);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const response = await apiClient.post('/copilot/chat', {
        business_id: selectedBizId,
        message: userMsg,
        question: userMsg
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.response || 'I have analyzed your request.',
          reasoning: response.reasoning || 'No details provided.',
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error communicating with the agent fleet. Please verify the backend is running.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12 h-[calc(100vh-140px)] flex flex-col">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">AI Executive Copilot</h1>
        <p className="mt-2 text-sm text-gray-500 font-medium">Confer with the CEO agent about strategies, KPI trends, or campaign reconciliations.</p>
      </div>

      {/* Chat Area Container */}
      <div className="flex-1 bg-white border border-gray-100 rounded-2xl shadow-sm overflow-hidden flex flex-col">
        {/* Messages */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6">
          {messages.map((msg, index) => (
            <div 
              key={index}
              className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
            >
              {/* Avatar */}
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0 select-none ${
                msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-900 text-white'
              }`}>
                {msg.role === 'user' ? 'U' : 'AI'}
              </div>

              {/* Bubble */}
              <div className="space-y-2">
                <div className={`rounded-2xl p-4 text-sm leading-relaxed ${
                  msg.role === 'user' 
                    ? 'bg-blue-50/70 border border-blue-100 text-blue-900' 
                    : 'bg-gray-50/50 border border-gray-100 text-gray-800'
                }`}>
                  {msg.content}
                </div>

                {/* Agent Reasoning Accordion */}
                {msg.reasoning && (
                  <details className="text-xs text-gray-500 bg-gray-50/30 border border-gray-100 rounded-xl p-3 cursor-pointer select-none">
                    <summary className="font-semibold text-gray-600 outline-none hover:text-gray-950 transition-colors">
                      View Executive Fleet Reasoning Path
                    </summary>
                    <p className="mt-2 pl-2 border-l border-gray-200 leading-relaxed text-gray-500 whitespace-pre-wrap">
                      {msg.reasoning}
                    </p>
                  </details>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-8 h-8 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-xs animate-pulse">AI</div>
              <div className="bg-gray-50 border border-gray-100 rounded-2xl p-4 text-sm text-gray-400 flex items-center gap-2">
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Form */}
        <form onSubmit={handleSend} className="p-4 border-t border-gray-100 flex gap-3 bg-gray-50/20">
          <input 
            type="text" 
            placeholder="Query the AI Leadership Council (e.g. 'How should we resolve the marketing spend conflict?')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            className="flex-1 rounded-xl border border-gray-200 p-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white"
          />
          <button 
            type="submit"
            disabled={!input.trim() || loading}
            className="rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-6 text-sm font-semibold text-white transition-all shadow-md"
          >
            Ask Fleet
          </button>
        </form>
      </div>
    </div>
  );
}
