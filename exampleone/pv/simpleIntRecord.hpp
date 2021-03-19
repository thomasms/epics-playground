#ifndef EPICS_EXAMPLES_ONE_HPP
#define EPICS_EXAMPLES_ONE_HPP

#include <iostream>
#include <pv/pvDatabase.h>
#include <pv/pvTimeStamp.h>
#include <pv/timeStamp.h>

#include <shareLib.h>

#include <pv/ntscalar.h>
#include <pv/pvDatabase.h>

using namespace epics;
using std::tr1::static_pointer_cast;

namespace epics {
namespace examples {
namespace one {

struct SimpleIntRecord;
typedef std::tr1::shared_ptr<SimpleIntRecord> SimpleIntRecordPtr;

struct epicsShareClass SimpleIntRecord : public epics::pvDatabase::PVRecord {
  POINTER_DEFINITIONS(SimpleIntRecord);

  static SimpleIntRecordPtr create(const std::string &name) {

    nt::NTScalarBuilderPtr builder = nt::NTScalar::createBuilder();
    pvData::PVStructurePtr structure = builder->value(pvData::pvInt)
                                           ->addAlarm()
                                           ->addTimeStamp()
                                           ->addDisplay()
                                           ->addControl()
                                           ->createPVStructure();

    // default value of 42
    pvData::PVScalarPtr value(
        structure->getSubFieldT<pvData::PVScalar>("value"));
    value->putFrom<pvData::int32>(42);

    // this doesn't do what it says
    value->setImmutable();

    SimpleIntRecordPtr rec(new SimpleIntRecord(name, structure));
    rec->initPVRecord();

    return rec;
  }

  // gets called on a put, I think....
  void process() { std::cout << "SimpleIntRecord::Processing...\n"; }

  virtual ~SimpleIntRecord() {}

private:
  SimpleIntRecord(std::string const &name,
                  pvData::PVStructurePtr const &structure)
      : PVRecord(name, structure) {}
};

} // namespace one
} // namespace examples
} // namespace epics

#endif // EPICS_EXAMPLES_ONE_HPP
