# CS262

# Things to still do
## Wire Protocol
- 1.5 message case - client not receiving properly
- Printing situation:
  - Login successful printed 4 times (should be fixed - alyssa)
  - Normal message delivery printed 2 times (should be fixed - alyssa)
  - Then messages maybe(?) resent after a user logs back in when disconnected (should be fixed - alyssa)
- Disconnect login again as same person and it hangs(?)
- General disconnect handling (done on wire; is this done on grpc??)
- Change prompt for deletion - "Enter 0 to delete, enter anything else if not." (done)
- List accounts (done)
- Two people logging in to the same account from different laptops (done just errors out)
- Make regex consistent across grpc and wire
