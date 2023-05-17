#pragma once

#include <QtPlugin>
#include <thread>
#include <chrono>
#include "PlotJuggler/datastreamer_base.h"

#include <zcm/zcm-cpp.hpp>

class ZcmDataStreamer : public PJ::DataStreamer
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "facontidavide.PlotJuggler3.DataStreamer")
    Q_INTERFACES(PJ::DataStreamer)

  public:
    ZcmDataStreamer();
    virtual ~ZcmDataStreamer();

    bool start(QStringList*) override;

    void shutdown() override;

    bool isRunning() const override;

    const char* name() const override;

    bool isDebugPlugin() override;

    bool xmlSaveState(QDomDocument& doc, QDomElement& parent_element) const override;

    bool xmlLoadState(const QDomElement& parent_element) override;

  private:
    bool _running;

    zcm::ZCM _zcm;

    zcm::Subscription* _subs;
    void handler(const zcm::ReceiveBuffer* rbuf, const std::string& channel);
};

