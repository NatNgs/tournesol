import { createListenerMiddleware } from '@reduxjs/toolkit';

import { RootState } from 'src/app/store';
import { isLoggedIn } from 'src/features/login/loginUtils';
import { fetchUserSettings } from 'src/features/settings/userSettingsSlice';

const loginSuccessfulListener = createListenerMiddleware();

/**
 * A Redux middleware that listens to successful authentications.
 *
 * After a log-in, fetch the user's settings from the API and save them in the
 * store.
 */
loginSuccessfulListener.startListening({
  predicate: (action, currentState, previousState) => {
    if (
      (currentState as RootState).token.status === 'idle' &&
      (previousState as RootState).token.status === 'loading'
    ) {
      if (isLoggedIn((currentState as RootState).token)) {
        return true;
      }
    }
    return false;
  },
  effect: async (action, listenerApi) => {
    listenerApi.dispatch(fetchUserSettings());
  },
});

export default loginSuccessfulListener;
