import React from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, TrendingUp, DollarSign, Clock } from 'lucide-react';
import { useShipmentContext } from '../contexts/ShipmentContext';

export const Recommendations: React.FC = () => {
  const { alerts } = useShipmentContext();

  const recommendations = alerts
    .filter((a: any) => a.risk_tier === 'CRITICAL' || a.risk_tier === 'HIGH')
    .map((alert: any) => ({
      shipment_id: alert.shipment_id,
      risk_tier: alert.risk_tier,
      action: alert.risk_tier === 'CRITICAL' ? 'MODE_SWITCH_AIR' : 'REROUTE',
      description: alert.risk_tier === 'CRITICAL'
        ? 'Upgrade to air freight to recover time against SLA'
        : 'Divert shipment to alternative transit path',
      cost_impact: alert.risk_tier === 'CRITICAL' ? 'High' : 'Medium',
      time_saving: alert.risk_tier === 'CRITICAL' ? '24-96 hours' : '12-48 hours',
      confidence: alert.delay_probability >= 0.8 ? 'High' : 'Medium',
    }));

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">Smart Recommendations</h2>
        <p className="text-light">AI-powered intervention suggestions for at-risk shipments</p>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {recommendations.length === 0 ? (
          <div className="card text-center py-12">
            <Lightbulb className="w-12 h-12 text-light mx-auto mb-4" />
            <p className="text-light">No recommendations at this time</p>
            <p className="text-sm text-light mt-2">All shipments are on track</p>
          </div>
        ) : (
          recommendations.map((rec: any, index: number) => (
            <motion.div
              key={rec.shipment_id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="card hover:border-accent"
            >
              <div className="flex items-start space-x-4">
                <div className="p-3 rounded-lg bg-gradient-to-br from-accent to-secondary">
                  <Lightbulb className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-1">{rec.shipment_id}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${
                        rec.risk_tier === 'CRITICAL' ? 'bg-risk-critical' : 'bg-risk-high'
                      }`}>
                        {rec.risk_tier} RISK
                      </span>
                    </div>
                    <span className="text-sm glass-light px-3 py-1 rounded-lg text-accent font-semibold">
                      {rec.confidence} Confidence
                    </span>
                  </div>

                  <div className="glass-light p-4 rounded-lg mb-4">
                    <h4 className="font-semibold text-white mb-2">Recommended Action: {rec.action}</h4>
                    <p className="text-sm text-light">{rec.description}</p>
                  </div>

                  <div className="grid grid-cols-3 gap-4 mb-4">
                    <div className="flex items-center space-x-2">
                      <DollarSign className="w-4 h-4 text-accent" />
                      <div>
                        <p className="text-xs text-light">Cost Impact</p>
                        <p className="text-sm font-semibold text-white">{rec.cost_impact}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock className="w-4 h-4 text-accent" />
                      <div>
                        <p className="text-xs text-light">Time Saving</p>
                        <p className="text-sm font-semibold text-white">{rec.time_saving}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <TrendingUp className="w-4 h-4 text-accent" />
                      <div>
                        <p className="text-xs text-light">SLA Impact</p>
                        <p className="text-sm font-semibold text-white">High</p>
                      </div>
                    </div>
                  </div>

                  <button className="btn-primary w-full">Execute Intervention</button>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  );
};
