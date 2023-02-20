import React from 'react';
import { useTranslation } from 'react-i18next';

import { Button, Link, Stack, Typography, Box, Divider } from '@mui/material';
import Grid2 from '@mui/material/Unstable_Grid2/Grid2';
import makeStyles from '@mui/styles/makeStyles';

import { ContentHeader, ContentBox } from 'src/components';
import TitledPaper from 'src/components/TitledPaper';
import FundingSection from 'src/pages/home/videos/sections/FundingSection';
import { utipTournesolUrl, paypalDonateTournesolUrl } from 'src/utils/url';

const useStyles = makeStyles(() => ({
  bankingInfo: {
    margin: 0,
  },
}));

const DonatePage = () => {
  const classes = useStyles();
  const { t } = useTranslation();

  const donateSectionSx = {
    width: '100%',
  };

  return (
    <>
      <ContentHeader title={`${t('menu.about')} > ${t('menu.donate')}`} />
      <ContentBox maxWidth="lg">
        <Grid2
          container
          width="100%"
          gap={6}
          flexDirection="column"
          alignItems="center"
        >
          <Grid2 sx={donateSectionSx}>
            <FundingSection linkToDonatePage={false} fullWidth />
          </Grid2>
          <Grid2 sx={donateSectionSx}>
            <TitledPaper title={t('about.donateHowTo')}>
              <Grid2
                container
                gap={2}
                alignItems="stretch"
                justifyContent="space-evenly"
              >
                <Grid2 width="100%" xs={12} sm={12} md={5}>
                  <Stack
                    spacing={2}
                    direction="column"
                    alignItems="center"
                    justify-content="space-between"
                  >
                    <Link
                      href={utipTournesolUrl}
                      rel="noopener"
                      target="_blank"
                    >
                      <img
                        src="/logos/uTip_Logo.png"
                        alt="uTip logo"
                        height="110px"
                      />
                    </Link>

                    <Button
                      variant="contained"
                      href={utipTournesolUrl}
                      rel="noopener"
                      target="_blank"
                    >
                      {t('donate.donateWithUtip')}
                    </Button>
                  </Stack>
                </Grid2>
                <Grid2 width="100%" xs={12} sm={12} md={5}>
                  <Stack
                    spacing={2}
                    direction="column"
                    alignItems="center"
                    justify-content="space-between"
                  >
                    <Link
                      href={paypalDonateTournesolUrl}
                      rel="noopener"
                      target="_blank"
                      width="100%"
                    >
                      <img
                        src="/logos/PayPal_Logo.svg"
                        alt="PayPal logo"
                        height="110px"
                        width="100%"
                      />
                    </Link>
                    <Button
                      variant="contained"
                      href={paypalDonateTournesolUrl}
                      rel="noopener"
                      target="_blank"
                    >
                      {t('donate.donateWithPaypal')}
                    </Button>
                  </Stack>
                </Grid2>
              </Grid2>
            </TitledPaper>
          </Grid2>
          <Grid2 sx={donateSectionSx}>
            <TitledPaper title={t('donate.doYouPreferDirectTransfer')}>
              <Box>
                <Typography variant="h5" sx={{ marginBottom: 1 }}>
                  {t('about.donateByDirectTransferEUR')}
                </Typography>
                <pre className={classes.bankingInfo}>Association Tournesol</pre>
                <pre className={classes.bankingInfo}>Lausanne, Switzerland</pre>
                <pre className={classes.bankingInfo}>
                  IBAN: CH75 0900 0000 1570 7623 1
                </pre>
                <pre className={classes.bankingInfo}>BIC: POFICHBEXXX</pre>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box>
                <Typography variant="h5" sx={{ marginBottom: 1 }}>
                  {t('about.donateByDirectTransferCHF')}
                </Typography>
                <pre className={classes.bankingInfo}>Association Tournesol</pre>
                <pre className={classes.bankingInfo}>Lausanne, Switzerland</pre>
                <pre className={classes.bankingInfo}>
                  IBAN: CH42 0900 0000 1569 4102 5
                </pre>
                <pre className={classes.bankingInfo}>BIC: POFICHBEXXX</pre>
              </Box>
            </TitledPaper>
          </Grid2>
        </Grid2>
      </ContentBox>
    </>
  );
};

export default DonatePage;
