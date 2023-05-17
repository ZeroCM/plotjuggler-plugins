#include "DataStreamZcm.hpp"
#include <QTextStream>
#include <QFile>
#include <QMessageBox>
#include <QDebug>
#include <thread>
#include <mutex>
#include <chrono>
#include <thread>
#include <math.h>

using namespace PJ;

ZcmDataStreamer::ZcmDataStreamer() : _running(false), _zcm("")
{
    _subs = _zcm.subscribe("EXAMPLE", &ZcmDataStreamer::handler, this);
    // Create 10 numeric series
    for (int i = 0; i < 10; i++)
    {
        auto str = QString("data_vect/%1").arg(i).toStdString();
        dataMap().addNumeric(str)->second;
    }
}

ZcmDataStreamer::~ZcmDataStreamer()
{
    shutdown();
    _zcm.unsubscribe(_subs);
    _subs = nullptr;
}

void ZcmDataStreamer::handler(const zcm::ReceiveBuffer* rbuf, const std::string& channel)
{
}

bool ZcmDataStreamer::start(QStringList*)
{
    if (!_zcm.good()) return false;
    _running = true;
    _zcm.start();
    return true;
}

void ZcmDataStreamer::shutdown()
{
    _running = false;
    _zcm.stop();
}

bool ZcmDataStreamer::isRunning() const
{
    return _running;
}

const char* ZcmDataStreamer::name() const
{
    return "Zcm Streamer";
}

bool ZcmDataStreamer::isDebugPlugin()
{
    return false;
}

bool ZcmDataStreamer::xmlSaveState(QDomDocument& doc, QDomElement& parent_element) const
{
    return true;
}

bool ZcmDataStreamer::xmlLoadState(const QDomElement& parent_element)
{
    return true;
}
