#include <iostream>
#include <string>
#include <vector>

#include <pv/channelProviderLocal.h>
#include <pv/serverContext.h>

#include <pv/simpleIntRecord.hpp>

using std::tr1::static_pointer_cast;
using namespace epics::pvData;
using namespace epics::pvAccess;
using namespace epics::pvDatabase;
using namespace epics::examples::one;

int main(int argc, char *argv[]) {

  PVDatabasePtr db = PVDatabase::getMaster();
  ChannelProviderLocalPtr provider = getChannelProviderLocal();

  const std::string recname = "examples:one:dummy";
  bool result = db->addRecord(SimpleIntRecord::create(recname));
  if (!result) {
    std::cout << "Could not add record: " << recname << " !\n";
    return 1;
  }

  ServerContext::shared_pointer ctx = startPVAServer("local", 0, true, true);

  std::cout << "ExampleOne - Database entries....\n";

  PVStringArrayPtr pvNames = db->getRecordNames();
  PVStringArray::const_svector xxx = pvNames->view();
  for (auto &e : pvNames->view())
    std::cout << e << "\n";

  std::string str;
  while (true) {
    std::cout << "Type 'exit' to quit \n";
    std::getline(std::cin, str);
    if (str.compare("exit") == 0)
      break;
  }

  return 0;
}